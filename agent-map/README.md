# Agent Map DA Flow

Put CSV, XLSX, JSON, or SQLite files into `agent-map/data/inbox/` and run:

```bash
python3 agent-map/pipeline/run_da_flow.py
```

What gets generated:

- `agent-map/runs/latest/status.json`: pipeline status for the dashboard
- `agent-map/runs/latest/outputs/index.json`: output catalog and preview payloads
- `agent-map/runs/latest/outputs/*.md|*.json|*.png`: generated analysis artifacts

Dashboard:

- Open `agent-map/dashboard.html` through a local static server or GitHub Pages
- The page reads `runs/latest` and renders input metadata, stage monitoring, and output previews

Notes:

- If `data/inbox/` is empty, the pipeline falls back to `data/samples/sample_sales.csv`
- The current implementation supports CSV, Excel, JSON, and SQLite inputs
