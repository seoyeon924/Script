# Agent Map DA Flow

Put CSV, XLSX, JSON, or SQLite files into `agent-map/data/inbox/` and run:

```bash
python3 agent-map/pipeline/run_da_flow.py
```

Generate Tableau planning and workbook artifacts from the latest run:

```bash
python3 agent-map/pipeline/generate_tableau_workbook.py
```

What gets generated:

- `agent-map/runs/latest/status.json`: pipeline status for the dashboard
- `agent-map/runs/latest/outputs/index.json`: output catalog and preview payloads
- `agent-map/runs/latest/outputs/*.md|*.json|*.png`: generated analysis artifacts
- `agent-map/runs/latest/outputs/tableau/*`: Tableau design brief, metric framework, wireframe, `twb`, and `twbx`

Dashboard:

- Open `agent-map/dashboard.html` through a local static server or GitHub Pages
- The page reads `runs/latest` and renders input metadata, stage monitoring, and output previews

Notes:

- If `data/inbox/` is empty, the pipeline falls back to `data/samples/sample_sales.csv`
- The current implementation supports CSV, Excel, JSON, and SQLite inputs
- The Tableau generator creates a workbook scaffold and packaged workbook based on the latest DA outputs and local text-file datasource
- Tableau Desktop validation is not run in this environment, so workbook compatibility should be verified in Tableau after generation
