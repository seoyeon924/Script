from __future__ import annotations

import argparse
import json
import math
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_DIR = ROOT / "data" / "inbox"
SAMPLE_INPUT = ROOT / "data" / "samples" / "sample_sales.csv"
RUNS_DIR = ROOT / "runs"
LATEST_DIR = RUNS_DIR / "latest"

STAGE_DEFS = [
    {"id": "data-ingestion", "name": "@data-ingestion", "icon": "⊕", "color": "mint"},
    {"id": "eda", "name": "@eda", "icon": "◈", "color": "lavender"},
    {"id": "problem", "name": "@problem", "icon": "✦", "color": "rose"},
    {"id": "metrics", "name": "@metrics", "icon": "▣", "color": "cream"},
    {"id": "analysis", "name": "@analysis", "icon": "⌘", "color": "mint"},
    {"id": "dashboard", "name": "@dashboard", "icon": "▦", "color": "lavender"},
    {"id": "report", "name": "@report", "icon": "≡", "color": "mint"},
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    return (
        value.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
    )


def format_compact_number(value: float) -> str:
    abs_value = abs(value)
    if abs_value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if abs_value >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"


def format_percent(value: float) -> str:
    return f"{value:.1f}%"


def ensure_dirs(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def clean_column_name(column: str) -> str:
    return slugify(column).strip("_")


def detect_file_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".csv"}:
        return "csv"
    if suffix in {".xlsx", ".xls"}:
        return "excel"
    if suffix in {".json"}:
        return "json"
    if suffix in {".db", ".sqlite", ".sqlite3"}:
        return "sqlite"
    raise ValueError(f"Unsupported input file: {path.name}")


def load_input_dataframe(path: Path) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    file_type = detect_file_type(path)
    metadata: Dict[str, Any] = {"name": path.name, "type": file_type, "size_bytes": path.stat().st_size}

    if file_type == "csv":
        df = pd.read_csv(path)
    elif file_type == "excel":
        xls = pd.ExcelFile(path)
        sheet_names = xls.sheet_names
        metadata["sheets"] = sheet_names
        df = pd.read_excel(path, sheet_name=sheet_names[0])
    elif file_type == "json":
        df = pd.read_json(path)
    else:
        import sqlite3

        conn = sqlite3.connect(path)
        try:
            tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", conn)
            if tables.empty:
                raise ValueError(f"No tables found in database {path.name}")
            table_name = tables.iloc[0]["name"]
            metadata["table"] = table_name
            df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)
        finally:
            conn.close()

    df.columns = [clean_column_name(str(col)) for col in df.columns]
    metadata["rows"] = int(len(df))
    metadata["columns"] = int(len(df.columns))
    metadata["column_names"] = list(df.columns)
    return df, metadata


def infer_date_column(df: pd.DataFrame) -> Optional[str]:
    for column in df.columns:
        if "date" in column or "month" in column:
            try:
                parsed = pd.to_datetime(df[column], errors="coerce")
                if parsed.notna().mean() > 0.7:
                    df[column] = parsed
                    return column
            except Exception:
                continue
    return None


def infer_metric_columns(df: pd.DataFrame) -> Dict[str, Optional[str]]:
    columns = set(df.columns)
    def pick(*names: str) -> Optional[str]:
        for name in names:
            if name in columns:
                return name
        return None

    return {
        "revenue": pick("revenue", "sales", "amount", "gmv"),
        "cost": pick("cost", "spend", "expense"),
        "orders": pick("orders", "conversions", "purchases"),
        "visitors": pick("visitors", "sessions", "users"),
        "segment": pick("segment", "customer_segment"),
        "category": pick("category", "product_category"),
        "sub_category": pick("sub_category", "subcategory"),
        "region": pick("region", "market", "country"),
        "channel": pick("channel", "source", "campaign"),
        "test_group": pick("test_group", "variant", "experiment_group"),
    }


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def render_markdown_preview(title: str, badge: str, metrics: List[Dict[str, str]], insights: List[str]) -> Dict[str, Any]:
    return {
        "kind": "report",
        "title": title,
        "badge": badge,
        "metrics": metrics[:3],
        "insights": insights[:5],
    }


def render_json_preview(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"kind": "json", "payload": payload}


def render_questions_preview(questions: List[str]) -> Dict[str, Any]:
    return {"kind": "questions", "questions": questions[:5]}


def render_chart_preview(title: str, image_path: str, caption: str) -> Dict[str, Any]:
    return {"kind": "image", "title": title, "image_path": image_path, "caption": caption}


def render_action_plan_preview(actions: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"kind": "action-plan", "actions": actions[:5]}


def replace_run_paths(value: Any, run_id: str) -> Any:
    if isinstance(value, dict):
        return {key: replace_run_paths(item, run_id) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_run_paths(item, run_id) for item in value]
    if isinstance(value, str):
        return value.replace(f"runs/{run_id}/", "runs/latest/")
    return value


@dataclass
class RunContext:
    run_id: str
    run_dir: Path
    status_path: Path
    outputs_dir: Path
    plots_dir: Path
    input_dir: Path
    output_manifest: List[Dict[str, Any]]
    status: Dict[str, Any]

    def save_status(self) -> None:
        write_json(self.status_path, self.status)

    def set_stage(self, stage_id: str, stage_status: str, summary: str) -> None:
        self.status["current_stage"] = stage_id
        for stage in self.status["stages"]:
            if stage["id"] == stage_id:
                stage["status"] = stage_status
                stage["summary"] = summary
                if stage_status == "processing":
                    stage["started_at"] = stage.get("started_at") or now_iso()
                if stage_status in {"completed", "failed"}:
                    stage["completed_at"] = now_iso()
                    started = stage.get("started_at")
                    if started:
                        delta = datetime.fromisoformat(stage["completed_at"]) - datetime.fromisoformat(started)
                        stage["duration_seconds"] = round(delta.total_seconds(), 2)
                break
        completed_count = len([s for s in self.status["stages"] if s["status"] == "completed"])
        self.status["progress"] = {"completed": completed_count, "total": len(self.status["stages"])}
        self.save_status()

    def add_output(self, item: Dict[str, Any]) -> None:
        self.output_manifest.append(item)
        write_json(self.outputs_dir / "index.json", {"run_id": self.run_id, "outputs": self.output_manifest})


def init_run(input_dir: Path, run_label: Optional[str] = None) -> RunContext:
    run_id = run_label or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_DIR / run_id
    outputs_dir = run_dir / "outputs"
    plots_dir = outputs_dir / "plots"
    ensure_dirs(run_dir, outputs_dir, plots_dir)

    stages = []
    for stage in STAGE_DEFS:
        stages.append(
            {
                "id": stage["id"],
                "name": stage["name"],
                "icon": stage["icon"],
                "color": stage["color"],
                "status": "pending",
                "summary": "Pending",
                "started_at": None,
                "completed_at": None,
                "duration_seconds": None,
            }
        )

    status = {
        "run_id": run_id,
        "started_at": now_iso(),
        "finished_at": None,
        "overall_status": "processing",
        "current_stage": "data-ingestion",
        "inputs": [],
        "progress": {"completed": 0, "total": len(stages)},
        "stages": stages,
    }
    status_path = run_dir / "status.json"
    write_json(status_path, status)
    write_json(outputs_dir / "index.json", {"run_id": run_id, "outputs": []})
    return RunContext(
        run_id=run_id,
        run_dir=run_dir,
        status_path=status_path,
        outputs_dir=outputs_dir,
        plots_dir=plots_dir,
        input_dir=input_dir,
        output_manifest=[],
        status=status,
    )


def choose_input_file(input_dir: Path) -> Path:
    ensure_dirs(input_dir)
    candidates = sorted(
        [path for path in input_dir.iterdir() if path.is_file() and path.suffix.lower() in {".csv", ".xlsx", ".xls", ".json", ".db", ".sqlite", ".sqlite3"}]
    )
    if candidates:
        return candidates[0]
    return SAMPLE_INPUT


def plot_bar(df: pd.DataFrame, x: str, y: str, title: str, output_path: Path, color: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(df[x].astype(str), df[y], color=color)
    ax.set_title(title, fontsize=14)
    ax.tick_params(axis="x", rotation=20)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def top_group_summary(df: pd.DataFrame, group_col: str, value_col: str, ascending: bool = False) -> Tuple[str, float]:
    grouped = df.groupby(group_col, dropna=False)[value_col].sum().sort_values(ascending=ascending)
    top_name = str(grouped.index[0])
    top_value = float(grouped.iloc[0])
    return top_name, top_value


def proportion_z_test(success_a: float, total_a: float, success_b: float, total_b: float) -> Dict[str, float]:
    p1 = success_a / total_a if total_a else 0.0
    p2 = success_b / total_b if total_b else 0.0
    pooled = (success_a + success_b) / (total_a + total_b) if (total_a + total_b) else 0.0
    denominator = math.sqrt(max(pooled * (1 - pooled) * ((1 / total_a) + (1 / total_b)), 1e-9))
    z_score = (p2 - p1) / denominator if denominator else 0.0
    p_value = math.erfc(abs(z_score) / math.sqrt(2))
    return {"rate_a": p1, "rate_b": p2, "lift": p2 - p1, "z_score": z_score, "p_value": p_value}


def build_dashboard_spec(metrics: Dict[str, Any], artifacts: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "layout": "three-column-monitor",
        "headline_metrics": [
            {"label": "Revenue", "value": metrics["formatted_revenue"]},
            {"label": "Profit", "value": metrics["formatted_profit"]},
            {"label": "Margin", "value": metrics["formatted_margin"]},
        ],
        "charts": [
            {"title": "Revenue by Category", "type": "bar", "asset": artifacts.get("category_chart")},
            {"title": "Revenue by Region", "type": "bar", "asset": artifacts.get("region_chart")},
            {"title": "Monthly Revenue Trend", "type": "bar", "asset": artifacts.get("monthly_chart")},
        ],
    }


def build_knowledge_base(
    profile: Dict[str, Any],
    metrics_payload: Dict[str, Any],
    analysis_insights: List[str],
    actions: List[Dict[str, Any]],
    ab_test_payload: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    rules = [
        "Prioritize low-margin categories for pricing review before acquisition spend increases.",
        "Promote segment-region combinations that outperform both on revenue and margin.",
        "Translate every major insight into an explicit owner and next action.",
    ]
    if ab_test_payload:
        winner = ab_test_payload["group_b"] if ab_test_payload["conversion_rate_b_pct"] > ab_test_payload["conversion_rate_a_pct"] else ab_test_payload["group_a"]
        rules.append(f"Roll out experiment winner {winner} only after validating downstream profit impact.")

    memories = [
        {
            "title": "Dataset shape",
            "detail": f"{profile['rows']:,} rows across {profile['columns']} columns were processed in the latest run.",
        },
        {
            "title": "Revenue baseline",
            "detail": f"Revenue is {format_compact_number(metrics_payload['total_revenue'])} with {format_percent(metrics_payload['profit_margin_pct'])} margin.",
        },
        {
            "title": "Top analytical signal",
            "detail": analysis_insights[0] if analysis_insights else "Analysis completed without a standout insight.",
        },
    ]
    return {
        "title": "Knowledge Base",
        "subtitle": "Learns from each DA run and carries operating rules forward.",
        "badge": "Self-Improving",
        "memories": memories,
        "rules": rules,
        "action_count": len(actions),
    }


def run_pipeline(input_dir: Path, run_label: Optional[str] = None) -> RunContext:
    ctx = init_run(input_dir, run_label=run_label)
    input_file = choose_input_file(input_dir)

    copied_input = ctx.run_dir / "input" / input_file.name
    ensure_dirs(copied_input.parent)
    shutil.copy2(input_file, copied_input)

    df, input_meta = load_input_dataframe(input_file)
    date_col = infer_date_column(df)
    metric_cols = infer_metric_columns(df)
    numeric_cols = list(df.select_dtypes(include="number").columns)

    ctx.status["inputs"] = [
        {
            **input_meta,
            "source": str(input_file.relative_to(ROOT)),
            "active": True,
        }
    ]
    ctx.save_status()

    revenue_col = metric_cols["revenue"]
    cost_col = metric_cols["cost"]
    orders_col = metric_cols["orders"]
    visitors_col = metric_cols["visitors"]
    category_col = metric_cols["category"]
    segment_col = metric_cols["segment"]
    region_col = metric_cols["region"]
    test_group_col = metric_cols["test_group"]

    if revenue_col is None:
        raise ValueError("The dataset must include a revenue-like column such as revenue or sales.")

    if cost_col is None:
        df["cost"] = df[revenue_col] * 0.72
        cost_col = "cost"

    if orders_col is None and visitors_col is not None:
        df["orders"] = (df[visitors_col] * 0.12).round().astype(int)
        orders_col = "orders"

    df["profit"] = df[revenue_col] - df[cost_col]
    if date_col:
        df["month"] = pd.to_datetime(df[date_col], errors="coerce").dt.to_period("M").astype(str)

    artifacts: Dict[str, Optional[str]] = {}

    ctx.set_stage("data-ingestion", "processing", "Validating schema and inferring metric columns")
    profile = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "numeric_columns": numeric_cols,
        "categorical_columns": [col for col in df.columns if col not in numeric_cols][:10],
        "date_column": date_col,
        "metric_mapping": metric_cols,
        "missing_cells": int(df.isna().sum().sum()),
    }
    write_json(ctx.outputs_dir / "dataset_profile.json", profile)
    ctx.add_output(
        {
            "id": "dataset-profile",
            "name": "Dataset Profile",
            "file_name": "dataset_profile.json",
            "relative_path": f"runs/{ctx.run_id}/outputs/dataset_profile.json",
            "type": "json",
            "status": "ready",
            "icon_class": "metrics",
            "meta": f"{profile['rows']:,} rows · {profile['columns']} columns",
            "preview": render_json_preview(profile),
        }
    )
    ctx.set_stage("data-ingestion", "completed", f"Loaded {profile['rows']:,} rows and {profile['columns']} columns")

    ctx.set_stage("eda", "processing", "Profiling numeric distributions and business slices")
    numeric_summary = df[numeric_cols].describe().round(2).fillna(0).to_dict() if numeric_cols else {}
    missing_by_col = df.isna().sum().sort_values(ascending=False).head(5)
    top_missing = {str(k): int(v) for k, v in missing_by_col.items() if int(v) > 0}
    insights = []
    if category_col:
        top_category, top_category_revenue = top_group_summary(df, category_col, revenue_col)
        insights.append(f"{top_category} leads revenue at {format_compact_number(top_category_revenue)}.")
    if region_col:
        top_region, top_region_revenue = top_group_summary(df, region_col, revenue_col)
        insights.append(f"{top_region} is the strongest region by revenue at {format_compact_number(top_region_revenue)}.")
    worst_margin_text = None
    if category_col:
        margin_df = (
            df.groupby(category_col, dropna=False)[["profit", revenue_col]]
            .sum()
            .assign(margin=lambda frame: frame["profit"] / frame[revenue_col].replace(0, 1))
            .sort_values("margin")
        )
        if not margin_df.empty:
            worst_margin_name = str(margin_df.index[0])
            worst_margin_value = float(margin_df.iloc[0]["margin"] * 100)
            worst_margin_text = f"{worst_margin_name} has the weakest margin at {worst_margin_value:.1f}%."
            insights.append(worst_margin_text)

    eda_lines = [
        "# EDA Report",
        "",
        f"- Rows: {profile['rows']:,}",
        f"- Columns: {profile['columns']}",
        f"- Missing cells: {profile['missing_cells']:,}",
        f"- Numeric columns: {', '.join(numeric_cols) if numeric_cols else 'None'}",
        "",
        "## Key Insights",
    ] + [f"- {insight}" for insight in insights]
    if top_missing:
        eda_lines += ["", "## Missing Values", *[f"- {col}: {count}" for col, count in top_missing.items()]]
    eda_lines += ["", "## Numeric Summary", "```json", json.dumps(numeric_summary, indent=2), "```"]
    write_text(ctx.outputs_dir / "eda_report.md", "\n".join(eda_lines))

    if category_col:
        chart_df = df.groupby(category_col, dropna=False)[revenue_col].sum().reset_index().sort_values(revenue_col, ascending=False)
        category_chart = ctx.plots_dir / "revenue_by_category.png"
        plot_bar(chart_df, category_col, revenue_col, "Revenue by Category", category_chart, "#d7c8ea")
        artifacts["category_chart"] = f"runs/{ctx.run_id}/outputs/plots/{category_chart.name}"
        ctx.add_output(
            {
                "id": "eda-chart-category",
                "name": "Category Revenue Chart",
                "file_name": category_chart.name,
                "relative_path": artifacts["category_chart"],
                "type": "image",
                "status": "ready",
                "icon_class": "dashboard",
                "meta": "EDA chart preview",
                "preview": render_chart_preview("Revenue by Category", artifacts["category_chart"], "Auto-generated from the current run."),
            }
        )

    ctx.add_output(
        {
            "id": "eda-report",
            "name": "EDA Report",
            "file_name": "eda_report.md",
            "relative_path": f"runs/{ctx.run_id}/outputs/eda_report.md",
            "type": "markdown",
            "status": "ready",
            "icon_class": "eda",
            "meta": f"{len(insights)} insights · {profile['rows']:,} rows",
            "preview": render_markdown_preview(
                "EDA Report",
                "Completed",
                [
                    {"value": f"{profile['rows']:,}", "label": "Rows"},
                    {"value": f"{profile['columns']}", "label": "Columns"},
                    {"value": f"{profile['missing_cells']:,}", "label": "Missing"},
                ],
                insights or ["Initial profiling completed."],
            ),
        }
    )
    ctx.set_stage("eda", "completed", f"Built EDA report with {len(insights)} core findings")

    ctx.set_stage("problem", "processing", "Generating business questions and hypotheses")
    questions = [
        "Which segment drives the best revenue efficiency and should receive more budget?",
        "Which category has the weakest profit margin and requires pricing or cost intervention?",
        "Which region is underperforming relative to its traffic volume?",
        "What trend changes appear in the latest month compared with the prior period?",
        "Which channel or experiment variant should be scaled next quarter?",
    ]
    hypotheses = [
        "Higher discounts appear to correlate with weaker profit margin in low-performing categories.",
        "Regional variance likely reflects different channel mixes and average order values.",
        "Variant B may improve conversion rate without improving downstream margin.",
    ]
    problem_md = "\n".join(
        ["# Problem Definition", "", "## Business Questions"] + [f"- {question}" for question in questions] + ["", "## Hypotheses"] + [f"- {item}" for item in hypotheses]
    )
    write_text(ctx.outputs_dir / "problem_definition.md", problem_md)
    ctx.add_output(
        {
            "id": "business-questions",
            "name": "Business Questions",
            "file_name": "problem_definition.md",
            "relative_path": f"runs/{ctx.run_id}/outputs/problem_definition.md",
            "type": "markdown",
            "status": "ready",
            "icon_class": "questions",
            "meta": f"{len(questions)} questions generated",
            "preview": render_questions_preview(questions),
        }
    )
    ctx.set_stage("problem", "completed", f"Generated {len(questions)} questions and {len(hypotheses)} hypotheses")

    ctx.set_stage("metrics", "processing", "Calculating KPI layer and conversion benchmarks")
    total_revenue = float(df[revenue_col].sum())
    total_cost = float(df[cost_col].sum())
    total_profit = float(df["profit"].sum())
    margin = (total_profit / total_revenue) * 100 if total_revenue else 0.0
    total_orders = float(df[orders_col].sum()) if orders_col else 0.0
    total_visitors = float(df[visitors_col].sum()) if visitors_col else 0.0
    conversion_rate = (total_orders / total_visitors) * 100 if total_visitors else 0.0
    avg_order_value = total_revenue / total_orders if total_orders else 0.0
    metrics_payload = {
        "total_revenue": round(total_revenue, 2),
        "total_cost": round(total_cost, 2),
        "total_profit": round(total_profit, 2),
        "profit_margin_pct": round(margin, 2),
        "avg_order_value": round(avg_order_value, 2),
        "total_orders": int(total_orders),
        "total_visitors": int(total_visitors),
        "conversion_rate_pct": round(conversion_rate, 2),
        "row_count": int(len(df)),
    }
    write_json(ctx.outputs_dir / "kpi_summary.json", metrics_payload)

    ab_test_payload = None
    if test_group_col and visitors_col and orders_col and df[test_group_col].nunique(dropna=True) >= 2:
        group_stats = df.groupby(test_group_col)[[orders_col, visitors_col]].sum().reset_index()
        if len(group_stats) >= 2:
            first = group_stats.iloc[0]
            second = group_stats.iloc[1]
            z_test = proportion_z_test(
                float(first[orders_col]),
                float(first[visitors_col]),
                float(second[orders_col]),
                float(second[visitors_col]),
            )
            ab_test_payload = {
                "group_a": str(first[test_group_col]),
                "group_b": str(second[test_group_col]),
                "conversion_rate_a_pct": round(z_test["rate_a"] * 100, 2),
                "conversion_rate_b_pct": round(z_test["rate_b"] * 100, 2),
                "lift_pct_point": round(z_test["lift"] * 100, 2),
                "z_score": round(z_test["z_score"], 3),
                "p_value": round(z_test["p_value"], 4),
                "significant_at_95": bool(z_test["p_value"] < 0.05),
            }
            write_json(ctx.outputs_dir / "ab_test_summary.json", ab_test_payload)

    metric_preview_payload = {
        **metrics_payload,
        "formatted_revenue": format_compact_number(total_revenue),
        "formatted_profit": format_compact_number(total_profit),
        "formatted_margin": format_percent(margin),
    }
    ctx.add_output(
        {
            "id": "kpi-summary",
            "name": "KPI Summary",
            "file_name": "kpi_summary.json",
            "relative_path": f"runs/{ctx.run_id}/outputs/kpi_summary.json",
            "type": "json",
            "status": "ready",
            "icon_class": "metrics",
            "meta": f"{metric_preview_payload['formatted_revenue']} revenue · {metric_preview_payload['formatted_margin']} margin",
            "preview": render_json_preview(metric_preview_payload),
        }
    )
    if ab_test_payload:
        ctx.add_output(
            {
                "id": "ab-test-summary",
                "name": "A/B Test",
                "file_name": "ab_test_summary.json",
                "relative_path": f"runs/{ctx.run_id}/outputs/ab_test_summary.json",
                "type": "json",
                "status": "ready",
                "icon_class": "questions",
                "meta": f"{ab_test_payload['group_b']} vs {ab_test_payload['group_a']} · p={ab_test_payload['p_value']}",
                "preview": render_json_preview(ab_test_payload),
            }
        )
    ctx.set_stage("metrics", "completed", f"Calculated KPI layer and {'A/B test summary' if ab_test_payload else 'core benchmarks'}")

    ctx.set_stage("analysis", "processing", "Running segment, regional, and time-series analysis")
    analysis_insights = []
    if segment_col:
        seg_df = df.groupby(segment_col)[revenue_col].sum().sort_values(ascending=False)
        if not seg_df.empty:
            seg_name = str(seg_df.index[0])
            seg_value = float(seg_df.iloc[0])
            analysis_insights.append(f"{seg_name} is the top segment by revenue at {format_compact_number(seg_value)}.")
    if region_col:
        region_df = (
            df.groupby(region_col)[["profit", revenue_col]]
            .sum()
            .assign(margin=lambda frame: frame["profit"] / frame[revenue_col].replace(0, 1))
            .sort_values("margin", ascending=False)
        )
        if not region_df.empty:
            best_region = str(region_df.index[0])
            best_region_margin = float(region_df.iloc[0]["margin"] * 100)
            analysis_insights.append(f"{best_region} has the highest regional margin at {best_region_margin:.1f}%.")
        region_chart_df = df.groupby(region_col)[revenue_col].sum().reset_index().sort_values(revenue_col, ascending=False)
        region_chart = ctx.plots_dir / "revenue_by_region.png"
        plot_bar(region_chart_df, region_col, revenue_col, "Revenue by Region", region_chart, "#bfe4d7")
        artifacts["region_chart"] = f"runs/{ctx.run_id}/outputs/plots/{region_chart.name}"
    if "month" in df.columns:
        month_df = df.groupby("month")[revenue_col].sum().reset_index()
        if len(month_df) >= 2:
            latest = float(month_df.iloc[-1][revenue_col])
            prev = float(month_df.iloc[-2][revenue_col])
            growth = ((latest - prev) / prev * 100) if prev else 0.0
            analysis_insights.append(f"Latest month revenue changed {growth:+.1f}% versus the prior month.")
        monthly_chart = ctx.plots_dir / "monthly_revenue.png"
        plot_bar(month_df, "month", revenue_col, "Monthly Revenue Trend", monthly_chart, "#f2d8e0")
        artifacts["monthly_chart"] = f"runs/{ctx.run_id}/outputs/plots/{monthly_chart.name}"

    analysis_lines = ["# Analysis Report", "", "## Key Findings"] + [f"- {item}" for item in analysis_insights]
    if ab_test_payload:
        winner = ab_test_payload["group_b"] if ab_test_payload["conversion_rate_b_pct"] > ab_test_payload["conversion_rate_a_pct"] else ab_test_payload["group_a"]
        analysis_lines += ["", "## Experiment Readout", f"- Leading variant: {winner}", f"- p-value: {ab_test_payload['p_value']}"]
    write_text(ctx.outputs_dir / "analysis_report.md", "\n".join(analysis_lines))
    ctx.add_output(
        {
            "id": "analysis-report",
            "name": "Analysis Report",
            "file_name": "analysis_report.md",
            "relative_path": f"runs/{ctx.run_id}/outputs/analysis_report.md",
            "type": "markdown",
            "status": "ready",
            "icon_class": "report",
            "meta": f"{len(analysis_insights)} findings synthesized",
            "preview": render_markdown_preview(
                "Analysis Report",
                "Deep Dive",
                [
                    {"value": metric_preview_payload["formatted_revenue"], "label": "Revenue"},
                    {"value": metric_preview_payload["formatted_profit"], "label": "Profit"},
                    {"value": metric_preview_payload["formatted_margin"], "label": "Margin"},
                ],
                analysis_insights or ["Analysis completed."],
            ),
        }
    )
    ctx.set_stage("analysis", "completed", f"Completed {len(analysis_insights)} analytical findings")

    ctx.set_stage("dashboard", "processing", "Generating chart assets and dashboard spec")
    dashboard_spec = build_dashboard_spec(metric_preview_payload, artifacts)
    write_json(ctx.outputs_dir / "dashboard_spec.json", dashboard_spec)
    ctx.add_output(
        {
            "id": "dashboard-spec",
            "name": "Dashboard Spec",
            "file_name": "dashboard_spec.json",
            "relative_path": f"runs/{ctx.run_id}/outputs/dashboard_spec.json",
            "type": "json",
            "status": "ready",
            "icon_class": "dashboard",
            "meta": f"{len(dashboard_spec['charts'])} charts configured",
            "preview": render_json_preview(dashboard_spec),
        }
    )
    if artifacts.get("region_chart"):
        ctx.add_output(
            {
                "id": "region-chart",
                "name": "Regional Revenue Chart",
                "file_name": Path(artifacts["region_chart"]).name,
                "relative_path": artifacts["region_chart"],
                "type": "image",
                "status": "ready",
                "icon_class": "dashboard",
                "meta": "Dashboard chart asset",
                "preview": render_chart_preview("Revenue by Region", artifacts["region_chart"], "Used by dashboard spec."),
            }
        )
    ctx.set_stage("dashboard", "completed", "Dashboard spec and chart assets generated")

    ctx.set_stage("report", "processing", "Writing executive report and action plan")
    actions = [
        {
            "priority": 1,
            "title": "Reduce discount pressure in low-margin categories",
            "owner": "Pricing",
            "impact": "High",
            "reason": worst_margin_text or "Margin variance requires intervention.",
        },
        {
            "priority": 2,
            "title": "Scale the strongest segment-region mix",
            "owner": "Growth",
            "impact": "High",
            "reason": analysis_insights[0] if analysis_insights else "Top-performing segments should be amplified.",
        },
        {
            "priority": 3,
            "title": "Validate experiment winner before full rollout",
            "owner": "Product",
            "impact": "Medium",
            "reason": "A/B test summary is available and should be operationalized." if ab_test_payload else "Prepare an experiment plan using the KPI baseline.",
        },
    ]
    exec_summary = [
        "# Executive Report",
        "",
        "## Summary",
        f"- Revenue reached {metric_preview_payload['formatted_revenue']} with {metric_preview_payload['formatted_margin']} profit margin.",
        f"- Total profit is {metric_preview_payload['formatted_profit']} across {metrics_payload['total_orders']:,} orders.",
        "",
        "## Recommended Actions",
    ] + [f"- P{item['priority']}: {item['title']} ({item['owner']})" for item in actions]
    action_plan_lines = [
        "# Action Plan",
        "",
        "Prioritized next steps based on the latest DA run.",
        "",
    ]
    for item in actions:
        action_plan_lines += [
            f"## P{item['priority']} · {item['title']}",
            f"- Owner: {item['owner']}",
            f"- Impact: {item['impact']}",
            f"- Why now: {item['reason']}",
            "",
        ]

    write_text(ctx.outputs_dir / "executive_report.md", "\n".join(exec_summary))
    write_text(ctx.outputs_dir / "action_plan.md", "\n".join(action_plan_lines))
    write_json(ctx.outputs_dir / "action_plan.json", {"actions": actions})
    knowledge_base = build_knowledge_base(profile, metrics_payload, analysis_insights, actions, ab_test_payload)
    write_json(ctx.outputs_dir / "knowledge_base.json", knowledge_base)

    ctx.add_output(
        {
            "id": "executive-report",
            "name": "Executive Report",
            "file_name": "executive_report.md",
            "relative_path": f"runs/{ctx.run_id}/outputs/executive_report.md",
            "type": "markdown",
            "status": "ready",
            "icon_class": "report",
            "meta": f"{len(actions)} actions prioritized",
            "preview": render_markdown_preview(
                "Executive Report",
                "Ready",
                [
                    {"value": metric_preview_payload["formatted_revenue"], "label": "Revenue"},
                    {"value": metric_preview_payload["formatted_profit"], "label": "Profit"},
                    {"value": metric_preview_payload["formatted_margin"], "label": "Margin"},
                ],
                [item["title"] for item in actions],
            ),
        }
    )
    ctx.add_output(
        {
            "id": "action-plan",
            "name": "Action Plan",
            "file_name": "action_plan.md",
            "relative_path": f"runs/{ctx.run_id}/outputs/action_plan.md",
            "type": "markdown",
            "status": "ready",
            "icon_class": "report",
            "meta": "Prioritized next steps",
            "preview": render_action_plan_preview(actions),
        }
    )
    ctx.add_output(
        {
            "id": "knowledge-base",
            "name": "Knowledge Base",
            "file_name": "knowledge_base.json",
            "relative_path": f"runs/{ctx.run_id}/outputs/knowledge_base.json",
            "type": "json",
            "status": "ready",
            "icon_class": "questions",
            "meta": f"{knowledge_base['action_count']} actions remembered",
            "preview": render_json_preview(knowledge_base),
        }
    )
    ctx.set_stage("report", "completed", "Executive report and action plan completed")

    ctx.status["overall_status"] = "completed"
    ctx.status["current_stage"] = "done"
    ctx.status["finished_at"] = now_iso()
    ctx.save_status()
    write_json(ctx.run_dir / "manifest.json", {"run_id": ctx.run_id, "status_path": f"runs/{ctx.run_id}/status.json"})

    if LATEST_DIR.exists():
        shutil.rmtree(LATEST_DIR)
    shutil.copytree(ctx.run_dir, LATEST_DIR)
    latest_outputs_index = LATEST_DIR / "outputs" / "index.json"
    latest_index_payload = json.loads(latest_outputs_index.read_text(encoding="utf-8"))
    latest_index_payload["outputs"] = replace_run_paths(latest_index_payload["outputs"], ctx.run_id)
    write_json(latest_outputs_index, latest_index_payload)
    write_json(LATEST_DIR / "manifest.json", {"run_id": ctx.run_id, "status_path": "runs/latest/status.json"})
    return ctx


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AI Data Analyst OS pipeline.")
    parser.add_argument("--input-dir", default=str(DEFAULT_INPUT_DIR), help="Directory containing CSV/XLSX/JSON/SQLite inputs.")
    parser.add_argument("--run-label", default=None, help="Optional explicit run label.")
    args = parser.parse_args()

    ctx = run_pipeline(Path(args.input_dir), run_label=args.run_label)
    print(json.dumps({"run_id": ctx.run_id, "latest_dir": str(LATEST_DIR)}, indent=2))


if __name__ == "__main__":
    main()
