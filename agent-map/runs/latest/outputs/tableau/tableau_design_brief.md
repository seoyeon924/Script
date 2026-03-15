# Tableau Dashboard Design Brief

## Tone
Soft editorial BI with calm premium enterprise styling

## Layout
- Global navigation: Left dark sidebar with page tabs, filter controls, and narrative guidance
- Page flow:
  - Executive Overview
  - Drivers & Diagnostics
  - Action Board
  - Data Table

## Color System
- Canvas: `#EEF1F6`
- Sidebar: `#434C66`
- Card: `#FFFFFF`
- Headline: `#2F3442`
- Primary accent: `#6E78B7`
- Secondary accent: `#B9DCCD`
- Positive: `#5E9B73`
- Negative: `#D96C63`
- Warning: `#D6A65F`

## UX Rules
- Keep the first page executive-friendly: scan, compare, decide.
- Hide secondary filters until a user enters diagnostic mode.
- Use max/min annotations sparingly and consistently with positive/negative colors.
- Preserve whitespace and card grouping so the design reads like a premium Tableau dashboard.

## Page Structure
### Executive Overview
- Purpose: General > Specific headline scan for executives and team leads
- Zones:
  - KPI cards with sparkline and delta
  - Trend line section
  - Category and region comparison
  - Action summary card
### Drivers & Diagnostics
- Purpose: Reveal likely causes behind KPI changes
- Zones:
  - Funnel efficiency view
  - A/B test lift card
  - Region/category ranking with max/min emphasis
  - Knowledge base insights
### Action Board
- Purpose: Operational next steps for business owners
- Zones:
  - Prioritized action cards
  - Actionable leading indicators
  - Owner-based execution table
### Data Table
- Purpose: Verification page for raw aggregated records
- Zones:
  - Detailed text table
  - Download/export affordance

## Feedback
### Executive
- Current KPI set is solid, but without a stronger lead metric emphasis executives may overreact to lagging revenue only.
- Action zones should separate scale decisions from diagnostic context so the next move is unmistakable.
### Operator
- The dashboard needs a clear drill path from KPI card to category/region table to avoid dead-end summaries.
- Use filters for date, segment, region, and channel; anything more should be secondary or hidden by default.
### Visual_Designer
- The reference style works because the hierarchy is calm: soft canvas, dark navigation, pastel sections, strong typographic anchors.
- Avoid overusing saturated accents; reserve them for status, maximum/minimum annotations, and action prompts.
