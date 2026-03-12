from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path
from typing import Any, Dict, List
from xml.etree.ElementTree import Element, SubElement, ElementTree


ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = ROOT / "runs"
LATEST_DIR = RUNS_DIR / "latest"
OUTPUTS_DIR = LATEST_DIR / "outputs"
TABLEAU_DIR = OUTPUTS_DIR / "tableau"


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def ensure_dirs(*paths: Path) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def latest_input_file() -> Path:
    input_dir = LATEST_DIR / "input"
    candidates = sorted([path for path in input_dir.iterdir() if path.is_file()])
    if not candidates:
        raise FileNotFoundError("No input file found in runs/latest/input")
    return candidates[0]


def build_metric_framework(kpi: Dict[str, Any], ab_test: Dict[str, Any], analysis_text: str, knowledge: Dict[str, Any]) -> Dict[str, Any]:
    metrics = [
        {
            "name": "CTR / Attention Efficiency",
            "formula": "orders / visitors",
            "why": "Actionable leading indicator that moves faster than revenue and reveals funnel friction.",
            "action_plan": "If CTR or upper-funnel conversion weakens by segment or region, shift campaign/message mix before revenue drops.",
        },
        {
            "name": "Profit Margin",
            "formula": "profit / revenue",
            "why": "Protects the business from scaling low-quality volume.",
            "action_plan": "Review discount and cost mix for low-margin categories before increasing spend.",
        },
        {
            "name": "Average Order Value",
            "formula": "revenue / orders",
            "why": "Explains whether growth comes from pricing/basket size versus raw volume.",
            "action_plan": "Bundle high-value products and adjust upsell placements in stronger segments.",
        },
        {
            "name": "Experiment Lift",
            "formula": "variant_b_conversion - variant_a_conversion",
            "why": "Supports fast decision-making on UX or campaign changes with relative comparison.",
            "action_plan": "Scale the winning variant only if lift is significant and margin is preserved.",
        },
        {
            "name": "Revenue per Visitor",
            "formula": "revenue / visitors",
            "why": "Combines traffic quality and monetization into one practical efficiency metric.",
            "action_plan": "Reallocate traffic toward channels/regions with stronger revenue per visitor.",
        },
    ]

    chart_recommendations = [
        {
            "title": "Executive KPI Cards",
            "chart_type": "KPI cards with sparkline and comparison delta",
            "x_axis": "date",
            "y_axis": "Revenue, Profit Margin, Conversion Rate, AOV",
            "why_fit": "Matches the user’s reference style and gives executives an instant signal scan.",
            "caution": "Keep comparison windows consistent and annotate when the latest period is incomplete.",
        },
        {
            "title": "Revenue and Conversion Trend",
            "chart_type": "Dual-mode line chart with value/% toggle",
            "x_axis": "date",
            "y_axis": "revenue or conversion rate",
            "why_fit": "Supports General > Specific storytelling and shows whether topline changes are demand or efficiency-driven.",
            "caution": "Do not mix absolute and relative scales simultaneously without a clear toggle.",
        },
        {
            "title": "Category / Region Performance",
            "chart_type": "Ranked horizontal bar chart",
            "x_axis": "revenue per category or region",
            "y_axis": "category / region",
            "why_fit": "Easy side-by-side comparison and fast identification of max/min performers.",
            "caution": "Sort descending and highlight only one max/min pair to avoid visual clutter.",
        },
        {
            "title": "Opportunity Focus Table",
            "chart_type": "Text table with in-cell bars",
            "x_axis": "N/A",
            "y_axis": "N/A",
            "why_fit": "Gives operators an actionable worklist, similar to the user’s sales pipeline reference.",
            "caution": "Limit to top 10-20 rows and keep metrics aligned to a single decision question.",
        },
    ]

    critique = {
        "executive": [
            "Current KPI set is solid, but without a stronger lead metric emphasis executives may overreact to lagging revenue only.",
            "Action zones should separate scale decisions from diagnostic context so the next move is unmistakable.",
        ],
        "operator": [
            "The dashboard needs a clear drill path from KPI card to category/region table to avoid dead-end summaries.",
            "Use filters for date, segment, region, and channel; anything more should be secondary or hidden by default.",
        ],
        "viz_designer": [
            "The reference style works because the hierarchy is calm: soft canvas, dark navigation, pastel sections, strong typographic anchors.",
            "Avoid overusing saturated accents; reserve them for status, maximum/minimum annotations, and action prompts.",
        ],
    }

    actions = [
        "Increase attention on leading indicators before revenue erosion appears in month-end reporting.",
        "Bias spend and product focus toward high revenue-per-visitor combinations.",
        "Treat statistically significant experiment lift as operational input, not automatic rollout approval.",
    ]
    if ab_test:
        actions.append(
            f"Variant {ab_test['group_b'] if ab_test['conversion_rate_b_pct'] > ab_test['conversion_rate_a_pct'] else ab_test['group_a']} currently leads on conversion; validate downstream profitability before full release."
        )

    return {
        "problem_definition": "Diagnose which parts of the funnel and commercial mix are driving or constraining efficient growth.",
        "analysis_goal": "Move from descriptive performance reporting to operational decision-making with leading indicators and action guidance.",
        "expected_causes": knowledge.get("rules", []),
        "recommended_metrics": metrics,
        "chart_recommendations": chart_recommendations,
        "executive_feedback": critique["executive"],
        "operator_feedback": critique["operator"],
        "viz_feedback": critique["viz_designer"],
        "action_summary": actions,
        "context": {
            "revenue": kpi["total_revenue"],
            "margin_pct": kpi["profit_margin_pct"],
            "conversion_rate_pct": kpi["conversion_rate_pct"],
            "analysis_excerpt": analysis_text,
        },
    }


def build_tableau_spec(metric_framework: Dict[str, Any], kpi: Dict[str, Any], knowledge: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "workbook_name": "AgentMap Executive Performance Dashboard",
        "brand_tone": "Soft editorial BI with calm premium enterprise styling",
        "palette": {
            "canvas": "#EEF1F6",
            "sidebar": "#434C66",
            "card": "#FFFFFF",
            "headline": "#2F3442",
            "accent_primary": "#6E78B7",
            "accent_secondary": "#B9DCCD",
            "positive": "#5E9B73",
            "negative": "#D96C63",
            "warning": "#D6A65F",
            "highlight_max": "#6E78B7",
            "highlight_min": "#D96C63",
        },
        "layout": {
            "global_nav": "Left dark sidebar with page tabs, filter controls, and narrative guidance",
            "page_flow": [
                "Executive Overview",
                "Drivers & Diagnostics",
                "Action Board",
                "Data Table",
            ],
        },
        "filters": [
            "Date",
            "Region",
            "Segment",
            "Category",
            "Channel",
            "Experiment Variant",
        ],
        "dashboard_pages": [
            {
                "name": "Executive Overview",
                "purpose": "General > Specific headline scan for executives and team leads",
                "zones": [
                    "KPI cards with sparkline and delta",
                    "Trend line section",
                    "Category and region comparison",
                    "Action summary card",
                ],
            },
            {
                "name": "Drivers & Diagnostics",
                "purpose": "Reveal likely causes behind KPI changes",
                "zones": [
                    "Funnel efficiency view",
                    "A/B test lift card",
                    "Region/category ranking with max/min emphasis",
                    "Knowledge base insights",
                ],
            },
            {
                "name": "Action Board",
                "purpose": "Operational next steps for business owners",
                "zones": [
                    "Prioritized action cards",
                    "Actionable leading indicators",
                    "Owner-based execution table",
                ],
            },
            {
                "name": "Data Table",
                "purpose": "Verification page for raw aggregated records",
                "zones": [
                    "Detailed text table",
                    "Download/export affordance",
                ],
            },
        ],
        "titles": {
            "workbook": "Executive Performance Dashboard",
            "subtitle": "From growth signal to operational action",
            "sections": [
                "What changed",
                "What explains it",
                "Where to act next",
                "What data is behind it",
            ],
        },
        "storytelling": {
            "narrative": [
                "Start with signal strength through KPI cards and trend context.",
                "Move into diagnostic comparisons by category, region, and test variant.",
                "End with clear owner-based actions and a transparent data table.",
            ],
            "knowledge_hooks": knowledge.get("rules", []),
        },
        "kpis": [
            {"label": "Revenue", "value": kpi["total_revenue"]},
            {"label": "Profit Margin", "value": kpi["profit_margin_pct"]},
            {"label": "Conversion Rate", "value": kpi["conversion_rate_pct"]},
            {"label": "Average Order Value", "value": kpi["avg_order_value"]},
        ],
        "feedback": {
            "executive": metric_framework["executive_feedback"],
            "operator": metric_framework["operator_feedback"],
            "visual_designer": metric_framework["viz_feedback"],
        },
    }


def markdown_metric_framework(metric_framework: Dict[str, Any]) -> str:
    lines = [
        "# Tableau Metric Framework",
        "",
        f"## Problem Definition",
        metric_framework["problem_definition"],
        "",
        "## Analysis Goal",
        metric_framework["analysis_goal"],
        "",
        "## Expected Causes",
    ]
    lines.extend([f"- {item}" for item in metric_framework["expected_causes"]])
    lines.extend(["", "## Recommended Metrics"])
    for item in metric_framework["recommended_metrics"]:
        lines.extend(
            [
                f"### {item['name']}",
                f"- Formula: `{item['formula']}`",
                f"- Why it matters: {item['why']}",
                f"- Action plan: {item['action_plan']}",
                "",
            ]
        )
    lines.extend(["## Recommended Charts"])
    for chart in metric_framework["chart_recommendations"]:
        lines.extend(
            [
                f"### {chart['title']}",
                f"- Chart type: {chart['chart_type']}",
                f"- X-axis: {chart['x_axis']}",
                f"- Y-axis: {chart['y_axis']}",
                f"- Why it fits: {chart['why_fit']}",
                f"- Watch-out: {chart['caution']}",
                "",
            ]
        )
    lines.extend(["## Action Summary"])
    lines.extend([f"- {item}" for item in metric_framework["action_summary"]])
    return "\n".join(lines)


def markdown_design_brief(tableau_spec: Dict[str, Any]) -> str:
    palette = tableau_spec["palette"]
    lines = [
        "# Tableau Dashboard Design Brief",
        "",
        "## Tone",
        tableau_spec["brand_tone"],
        "",
        "## Layout",
        f"- Global navigation: {tableau_spec['layout']['global_nav']}",
        "- Page flow:",
    ]
    lines.extend([f"  - {page}" for page in tableau_spec["layout"]["page_flow"]])
    lines.extend(
        [
            "",
            "## Color System",
            f"- Canvas: `{palette['canvas']}`",
            f"- Sidebar: `{palette['sidebar']}`",
            f"- Card: `{palette['card']}`",
            f"- Headline: `{palette['headline']}`",
            f"- Primary accent: `{palette['accent_primary']}`",
            f"- Secondary accent: `{palette['accent_secondary']}`",
            f"- Positive: `{palette['positive']}`",
            f"- Negative: `{palette['negative']}`",
            f"- Warning: `{palette['warning']}`",
            "",
            "## UX Rules",
            "- Keep the first page executive-friendly: scan, compare, decide.",
            "- Hide secondary filters until a user enters diagnostic mode.",
            "- Use max/min annotations sparingly and consistently with positive/negative colors.",
            "- Preserve whitespace and card grouping so the design reads like a premium Tableau dashboard.",
            "",
            "## Page Structure",
        ]
    )
    for page in tableau_spec["dashboard_pages"]:
        lines.extend(
            [
                f"### {page['name']}",
                f"- Purpose: {page['purpose']}",
                "- Zones:",
            ]
        )
        lines.extend([f"  - {zone}" for zone in page["zones"]])
    lines.extend(["", "## Feedback"])
    for role, items in tableau_spec["feedback"].items():
        lines.append(f"### {role.title()}")
        lines.extend([f"- {item}" for item in items])
    return "\n".join(lines)


def build_wireframe_html(tableau_spec: Dict[str, Any], metric_framework: Dict[str, Any]) -> str:
    palette = tableau_spec["palette"]
    pages = tableau_spec["dashboard_pages"]
    first_page = pages[0]
    chart_cards = metric_framework["chart_recommendations"][:4]
    kpis = tableau_spec["kpis"]
    actions = metric_framework["action_summary"][:3]
    filters = tableau_spec["filters"][:4]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{tableau_spec['workbook_name']} Wireframe</title>
  <style>
    body {{
      margin: 0;
      font-family: Inter, system-ui, sans-serif;
      background: {palette['canvas']};
      color: {palette['headline']};
    }}
    .app {{
      display: grid;
      grid-template-columns: 280px 1fr;
      min-height: 100vh;
    }}
    .sidebar {{
      background: {palette['sidebar']};
      color: white;
      padding: 28px;
      display: flex;
      flex-direction: column;
      gap: 24px;
    }}
    .sidebar h1 {{ font-size: 34px; line-height: 1.05; margin: 0; }}
    .sidebar p {{ color: rgba(255,255,255,0.78); line-height: 1.6; }}
    .pill {{
      display: inline-block;
      padding: 10px 14px;
      border-radius: 999px;
      background: rgba(255,255,255,0.12);
      margin: 0 8px 8px 0;
      font-size: 13px;
    }}
    .main {{
      padding: 26px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}
    .hero {{
      background: rgba(255,255,255,0.72);
      border: 1px solid rgba(47,52,66,0.08);
      border-radius: 22px;
      padding: 24px;
    }}
    .hero h2 {{ margin: 0 0 8px; font-size: 40px; }}
    .hero p {{ margin: 0; color: #667085; max-width: 860px; line-height: 1.6; }}
    .kpis {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 16px;
    }}
    .kpi {{
      background: white;
      border-radius: 20px;
      padding: 18px;
      min-height: 140px;
      border: 1px solid rgba(47,52,66,0.08);
    }}
    .kpi small {{ color: #778; font-size: 12px; text-transform: uppercase; letter-spacing: .06em; }}
    .kpi strong {{ display: block; font-size: 36px; margin: 10px 0; }}
    .spark {{
      height: 58px;
      border-radius: 14px;
      background: linear-gradient(180deg, {palette['accent_primary']}66, {palette['accent_primary']}12);
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1.1fr 1fr;
      gap: 18px;
    }}
    .card {{
      background: rgba(255,255,255,0.72);
      border-radius: 22px;
      padding: 20px;
      border: 1px solid rgba(47,52,66,0.08);
    }}
    .card h3 {{ margin: 0 0 8px; font-size: 22px; }}
    .sub {{
      color: #6d7282;
      font-size: 13px;
      line-height: 1.6;
      margin-bottom: 16px;
    }}
    .bars, .actions {{ display: flex; flex-direction: column; gap: 10px; }}
    .bar-row {{
      display: grid;
      grid-template-columns: 160px 1fr 40px;
      gap: 10px;
      align-items: center;
      font-size: 13px;
    }}
    .track {{
      height: 16px;
      border-radius: 999px;
      background: #dfe5ef;
      overflow: hidden;
    }}
    .fill {{ height: 100%; background: {palette['accent_primary']}; }}
    .fill.min {{ background: {palette['negative']}; }}
    .action {{
      background: white;
      border-radius: 16px;
      padding: 14px;
      border-left: 5px solid {palette['accent_primary']};
    }}
    .tables {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 12px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th, td {{
      text-align: left;
      padding: 10px 8px;
      border-bottom: 1px solid rgba(47,52,66,0.08);
    }}
    .tag {{
      display: inline-block;
      background: {palette['accent_secondary']};
      color: {palette['headline']};
      border-radius: 999px;
      padding: 4px 10px;
      font-size: 11px;
      margin-right: 6px;
    }}
  </style>
</head>
<body>
  <div class="app">
    <aside class="sidebar">
      <div>
        <h1>Executive<br>Performance</h1>
        <p>{tableau_spec['titles']['subtitle']}</p>
      </div>
      <div>
        <div class="pill">Overview</div>
        <div class="pill">Diagnostics</div>
        <div class="pill">Action Board</div>
        <div class="pill">Data Table</div>
      </div>
      <div>
        <p><strong>Filters</strong></p>
        {''.join(f'<div class="pill">{item}</div>' for item in filters)}
      </div>
      <div>
        <p><strong>Design Notes</strong></p>
        <p>Dark navigation, editorial KPI cards, soft canvas, and restrained pastel accents modeled after your usual dashboard language.</p>
      </div>
    </aside>
    <main class="main">
      <section class="hero">
        <h2>{first_page['name']}</h2>
        <p>{first_page['purpose']}</p>
      </section>
      <section class="kpis">
        {''.join(f"<div class='kpi'><small>{item['label']}</small><strong>{item['value']}</strong><div class='spark'></div></div>" for item in kpis)}
      </section>
      <section class="grid">
        <div class="card">
          <h3>Performance Drivers</h3>
          <div class="sub">General > Specific flow with max/min emphasis and description under each chart.</div>
          <div class="bars">
            <div class="bar-row"><span>North America</span><div class="track"><div class="fill" style="width: 88%"></div></div><span>max</span></div>
            <div class="bar-row"><span>Asia Pacific</span><div class="track"><div class="fill" style="width: 74%"></div></div><span></span></div>
            <div class="bar-row"><span>Europe</span><div class="track"><div class="fill min" style="width: 42%"></div></div><span>min</span></div>
          </div>
        </div>
        <div class="card">
          <h3>Action Board</h3>
          <div class="sub">Actionable next moves surfaced in executive language.</div>
          <div class="actions">
            {''.join(f"<div class='action'>{item}</div>" for item in actions)}
          </div>
        </div>
      </section>
      <section class="card">
        <h3>Recommended Chart Set</h3>
        <div class="sub">These placeholders map directly to the Tableau workbook tabs and objects.</div>
        <div class="tables">
          <table>
            <thead><tr><th>Chart</th><th>Description</th><th>X</th><th>Y</th></tr></thead>
            <tbody>
              {''.join(f"<tr><td>{item['title']}</td><td>{item['why_fit']}</td><td>{item['x_axis']}</td><td>{item['y_axis']}</td></tr>" for item in chart_cards)}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""


def prettify_xml(elem: Element, level: int = 0) -> None:
    indent = "\n" + ("  " * level)
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        for child in elem:
            prettify_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent
    elif level and (not elem.tail or not elem.tail.strip()):
        elem.tail = indent


def build_twb_xml(tableau_spec: Dict[str, Any], input_file: Path) -> Element:
    workbook = Element(
        "workbook",
        {
            "original-version": "2024.1",
            "source-build": "agent-map-codex",
            "source-platform": "mac",
            "version": "2024.1",
        },
    )

    manifest = SubElement(workbook, "document-format-change-manifest")
    SubElement(manifest, "_.fcp.AccessibleZoneTabOrder.true...style")

    prefs = SubElement(workbook, "preferences")
    SubElement(prefs, "preference", {"name": "ui.encoding.shelf.height", "value": "24"})

    datasources = SubElement(workbook, "datasources")
    datasource = SubElement(
        datasources,
        "datasource",
        {
            "caption": "AgentMap Data",
            "inline": "true",
            "name": "federated.1",
            "version": "18.1",
        },
    )
    connection = SubElement(
        datasource,
        "connection",
        {
            "class": "textscan",
            "dbname": str(input_file.name),
            "directory": "Data",
            "filename": input_file.name,
        },
    )
    cols = [
        "date",
        "region",
        "segment",
        "category",
        "sub_category",
        "channel",
        "visitors",
        "orders",
        "revenue",
        "cost",
        "discount",
        "test_group",
    ]
    metadata = SubElement(datasource, "metadata-records")
    for name in cols:
        record = SubElement(metadata, "metadata-record", {"class": "column"})
        SubElement(record, "local-name").text = name
        SubElement(record, "remote-name").text = name
        SubElement(record, "remote-type").text = "real" if name in {"visitors", "orders", "revenue", "cost", "discount"} else "wstring"

    worksheets = SubElement(workbook, "worksheets")
    dashboard_names = [page["name"] for page in tableau_spec["dashboard_pages"]]
    for page in dashboard_names:
        worksheet = SubElement(worksheets, "worksheet", {"name": page})
        SubElement(worksheet, "layout-options")
        table = SubElement(worksheet, "table")
        view = SubElement(table, "view")
        datasource_deps = SubElement(view, "datasource-dependencies", {"datasource": "federated.1"})
        for item in tableau_spec["kpis"][:4]:
            column_name = item["label"].lower().replace(" ", "_")
            SubElement(
                datasource_deps,
                "column",
                {
                    "caption": item["label"],
                    "datatype": "real",
                    "name": f"[{column_name}]",
                    "role": "measure",
                    "type": "quantitative",
                },
            )

    dashboards = SubElement(workbook, "dashboards")
    for index, page in enumerate(tableau_spec["dashboard_pages"], start=1):
        dashboard = SubElement(dashboards, "dashboard", {"name": page["name"]})
        style = SubElement(dashboard, "style")
        SubElement(style, "style-rule", {"element": "dashboard"})
        zones = SubElement(dashboard, "zones")
        for zone_index, zone_name in enumerate(page["zones"], start=1):
            zone = SubElement(
                zones,
                "zone",
                {
                    "id": str(zone_index),
                    "name": zone_name,
                    "type-v2": "layout-basic",
                    "x": "0",
                    "y": str((zone_index - 1) * 120),
                    "w": "1200",
                    "h": "100",
                },
            )
            zone.text = zone_name

    windows = SubElement(workbook, "windows")
    SubElement(windows, "window", {"class": "dashboard", "name": tableau_spec["dashboard_pages"][0]["name"]})

    prettify_xml(workbook)
    return workbook


def package_twbx(twb_path: Path, input_file: Path, output_path: Path) -> None:
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(twb_path, arcname=twb_path.name)
        archive.write(input_file, arcname=f"Data/{input_file.name}")


def generate_tableau_assets() -> Dict[str, str]:
    ensure_dirs(TABLEAU_DIR)

    kpi = load_json(OUTPUTS_DIR / "kpi_summary.json")
    knowledge = load_json(OUTPUTS_DIR / "knowledge_base.json")
    ab_test = load_json(OUTPUTS_DIR / "ab_test_summary.json") if (OUTPUTS_DIR / "ab_test_summary.json").exists() else {}
    analysis_text = (OUTPUTS_DIR / "analysis_report.md").read_text(encoding="utf-8")

    metric_framework = build_metric_framework(kpi, ab_test, analysis_text, knowledge)
    tableau_spec = build_tableau_spec(metric_framework, kpi, knowledge)

    metric_framework_path = TABLEAU_DIR / "tableau_metric_framework.md"
    design_brief_path = TABLEAU_DIR / "tableau_design_brief.md"
    tableau_spec_path = TABLEAU_DIR / "tableau_spec.json"
    wireframe_path = TABLEAU_DIR / "tableau_wireframe.html"
    twb_path = TABLEAU_DIR / "agent_map_exec_dashboard.twb"
    twbx_path = TABLEAU_DIR / "agent_map_exec_dashboard.twbx"

    write_text(metric_framework_path, markdown_metric_framework(metric_framework))
    write_text(design_brief_path, markdown_design_brief(tableau_spec))
    write_json(tableau_spec_path, tableau_spec)
    write_text(wireframe_path, build_wireframe_html(tableau_spec, metric_framework))

    input_file = latest_input_file()
    workbook_xml = build_twb_xml(tableau_spec, input_file)
    ElementTree(workbook_xml).write(twb_path, encoding="utf-8", xml_declaration=True)

    packaged_input = TABLEAU_DIR / "Data"
    ensure_dirs(packaged_input)
    copied_data = packaged_input / input_file.name
    shutil.copy2(input_file, copied_data)
    package_twbx(twb_path, copied_data, twbx_path)

    manifest = {
        "metric_framework": str(metric_framework_path.relative_to(ROOT)),
        "design_brief": str(design_brief_path.relative_to(ROOT)),
        "tableau_spec": str(tableau_spec_path.relative_to(ROOT)),
        "wireframe": str(wireframe_path.relative_to(ROOT)),
        "twb": str(twb_path.relative_to(ROOT)),
        "twbx": str(twbx_path.relative_to(ROOT)),
    }
    write_json(TABLEAU_DIR / "manifest.json", manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Tableau design and workbook artifacts from the latest DA run.")
    parser.parse_args()
    manifest = generate_tableau_assets()
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
