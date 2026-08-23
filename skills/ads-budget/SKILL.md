---
name: ads-budget
description: Use when the user asks about budget allocation, bidding strategy, ad spend split, ROAS target, media budget, scaling campaigns, or which campaigns to kill. Evaluates spend distribution, bidding fit, and scaling readiness using the 70/20/10 rule, 3x Kill Rule, and 20% scaling rule.
---

# Budget Allocation & Bidding Strategy

## Process

1. Collect budget and performance data across all active platforms
2. Read `references/budget-allocation.md` for the platform selection matrix
3. Read `references/bidding-strategies.md` for per-platform decision trees
   and current AI bidding innovations
4. **Validate**: confirm spend data covers ≥14 days before evaluating kill/scale decisions
5. Evaluate budget allocation, bidding strategy, and scaling readiness
6. **Validate**: verify kill list candidates have sufficient data (≥20 clicks or ≥$100 spend) before recommending pause
7. Generate recommendations with kill list and scale list

## Budget Allocation Framework

### 70/20/10 Rule
- **70%** on proven channels (consistent ROAS/CPA targets met)
- **20%** on scaling channels (showing promise, need more data)
- **10%** on testing channels (new platforms, audiences, creatives)

Platform-by-business-type selection matrix (SaaS B2B, e-commerce, local
service, B2B enterprise, info products, mobile app, real estate, healthcare,
finance, agency) lives in `references/budget-allocation.md`.

### Budget Sufficiency Rules

| Platform | Minimum Daily | Learning Phase Budget |
|----------|--------------|----------------------|
| Google Search | $20/day | Sufficient for 15+ conv/month |
| Google PMax | $50/day | Sufficient for algorithm optimization |
| Meta | $20/day per ad set | ≥5x target CPA per ad set |
| LinkedIn | $50/day Sponsored Content | 15+ conversions/month |
| TikTok | $50/day campaign, $20/day ad group | ≥50x target CPA per ad group |
| Microsoft | No strict minimum | Sufficient for stable delivery |

## Bidding Strategy Evaluation

Match the bidding strategy to conversion volume and tracking maturity —
full per-platform decision trees (Google, Meta, LinkedIn, TikTok, Microsoft)
in `references/bidding-strategies.md`. Headline rule for Google:

- <30 conv/month → Maximize Clicks (cap CPC at benchmark)
- 30-50 conv/month → Maximize Conversions
- >50 conv/month → Target CPA
- Revenue tracking active + >50 conv/month → Target ROAS

Current AI bidding options worth evaluating (details and caveats in
`references/bidding-strategies.md`): Google AI Max for Search, TikTok Smart+
modular control, Apple Ads Maximize Conversions (GA Feb 2026), Meta
Advantage+ bidding.

## Scaling Assessment

### Ready to Scale (Green Light)
- CPA consistently below target for 2+ weeks
- ≥50 conversions per week (learning phase exited)
- CTR stable or improving
- ROAS above target
- No creative fatigue signals

### 20% Rule
Never increase budget by more than 20% at a time:
- Week 1: $100/day → $120/day
- Week 2: $120/day → $144/day
- Week 3: $144/day → $173/day
- Monitor 3-5 days after each increase for performance stability

### Scaling Methods
1. **Vertical**: increase budget on winning campaigns (20% rule)
2. **Horizontal**: duplicate winning campaigns to new audiences
3. **Platform expansion**: add budget on new platforms
4. **Geographic expansion**: test new markets/regions
5. **Format expansion**: test new ad formats on same platform

## Kill List Assessment

### 3x Kill Rule
- Any campaign/ad group with CPA >3x target → **flag for pause**
- Review spend in last 14 days with no conversions → **flag for pause**
- Creative with CTR >50% below platform benchmark → **flag for creative kill**

### Kill Decision Framework
| Scenario | Data Required | Action |
|----------|---------------|--------|
| CPA >3x target | ≥7 days data, ≥20 clicks | Pause immediately |
| No conversions | ≥$100 spend or ≥50 clicks | Pause and diagnose |
| CTR <50% of benchmark | ≥1,000 impressions | Kill creative, test new |
| ROAS <50% of target | ≥14 days data | Reduce budget 50% or pause |

## MER (Marketing Efficiency Ratio)

```
MER = Total Revenue / Total Marketing Spend
```

- Assess blended efficiency across all platforms
- Target MER varies by business: 3x-10x depending on margins
- Use MER to evaluate overall health, not just per-platform ROAS
- Incrementality testing recommended for MER accuracy

## Output

### Budget & Bidding Assessment

```
Budget Allocation Health

Allocation Strategy:  ████████░░  XX/100
Bidding Strategies:   ██████████  XX/100
Scaling Readiness:    ███████░░░  XX/100
Budget Sufficiency:   █████░░░░░  XX/100
```

### Deliverables
- `BUDGET-STRATEGY-REPORT.md`: Full allocation and bidding analysis
- Current vs recommended budget split (pie chart data)
- Bidding strategy recommendations per platform/campaign
- Scale list: campaigns ready for more budget
- Kill list: campaigns/ad groups to pause immediately
- MER analysis and trend
- Quick Wins for immediate budget optimization
