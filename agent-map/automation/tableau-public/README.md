# Tableau Public Web Authoring Prototype

This is a browser automation prototype for Tableau Public web authoring.

What it does:

- Opens Tableau Public in a real browser
- Reuses a stored login session
- Uploads the latest DA input file
- Captures screenshots and logs for each major step
- Leaves room for workbook creation and download steps

Important constraints:

- Tableau Public UI can change at any time
- Selectors and flows are intentionally conservative and may need adjustment
- This prototype does not guarantee a full workbook build yet
- Login credentials are not stored in git; use a persisted Playwright session

Setup:

```bash
cd agent-map/automation/tableau-public
npm install
npx playwright install chromium
```

Create a local session:

```bash
npm run auth
```

Run the prototype:

```bash
npm run run
```

Artifacts are written to:

- `agent-map/automation/tableau-public/artifacts/`

Config:

- Edit `src/config.js` if Tableau Public changes its upload or authoring URLs
