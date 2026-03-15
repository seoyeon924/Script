# Tableau Metric Framework

## Problem Definition
Diagnose which parts of the funnel and commercial mix are driving or constraining efficient growth.

## Analysis Goal
Move from descriptive performance reporting to operational decision-making with leading indicators and action guidance.

## Expected Causes
- Prioritize low-margin categories for pricing review before acquisition spend increases.
- Promote segment-region combinations that outperform both on revenue and margin.
- Translate every major insight into an explicit owner and next action.
- Roll out experiment winner B only after validating downstream profit impact.

## Recommended Metrics
### CTR / Attention Efficiency
- Formula: `orders / visitors`
- Why it matters: Actionable leading indicator that moves faster than revenue and reveals funnel friction.
- Action plan: If CTR or upper-funnel conversion weakens by segment or region, shift campaign/message mix before revenue drops.

### Profit Margin
- Formula: `profit / revenue`
- Why it matters: Protects the business from scaling low-quality volume.
- Action plan: Review discount and cost mix for low-margin categories before increasing spend.

### Average Order Value
- Formula: `revenue / orders`
- Why it matters: Explains whether growth comes from pricing/basket size versus raw volume.
- Action plan: Bundle high-value products and adjust upsell placements in stronger segments.

### Experiment Lift
- Formula: `variant_b_conversion - variant_a_conversion`
- Why it matters: Supports fast decision-making on UX or campaign changes with relative comparison.
- Action plan: Scale the winning variant only if lift is significant and margin is preserved.

### Revenue per Visitor
- Formula: `revenue / visitors`
- Why it matters: Combines traffic quality and monetization into one practical efficiency metric.
- Action plan: Reallocate traffic toward channels/regions with stronger revenue per visitor.

## Recommended Charts
### Executive KPI Cards
- Chart type: KPI cards with sparkline and comparison delta
- X-axis: date
- Y-axis: Revenue, Profit Margin, Conversion Rate, AOV
- Why it fits: Matches the user’s reference style and gives executives an instant signal scan.
- Watch-out: Keep comparison windows consistent and annotate when the latest period is incomplete.

### Revenue and Conversion Trend
- Chart type: Dual-mode line chart with value/% toggle
- X-axis: date
- Y-axis: revenue or conversion rate
- Why it fits: Supports General > Specific storytelling and shows whether topline changes are demand or efficiency-driven.
- Watch-out: Do not mix absolute and relative scales simultaneously without a clear toggle.

### Category / Region Performance
- Chart type: Ranked horizontal bar chart
- X-axis: revenue per category or region
- Y-axis: category / region
- Why it fits: Easy side-by-side comparison and fast identification of max/min performers.
- Watch-out: Sort descending and highlight only one max/min pair to avoid visual clutter.

### Opportunity Focus Table
- Chart type: Text table with in-cell bars
- X-axis: N/A
- Y-axis: N/A
- Why it fits: Gives operators an actionable worklist, similar to the user’s sales pipeline reference.
- Watch-out: Limit to top 10-20 rows and keep metrics aligned to a single decision question.

## Action Summary
- Increase attention on leading indicators before revenue erosion appears in month-end reporting.
- Bias spend and product focus toward high revenue-per-visitor combinations.
- Treat statistically significant experiment lift as operational input, not automatic rollout approval.
- Variant B currently leads on conversion; validate downstream profitability before full release.
