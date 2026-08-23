# Bidding Strategies — Decision Trees & AI Bidding Innovations

Reference for `smartpowers:ads-budget`.

## Google Ads Bidding Decision Tree

```
Start
├─ <30 conversions/month?
│  └─ Use Maximize Clicks (cap CPC at benchmark)
│     └─ When >30 conv/month → Maximize Conversions
├─ 30-50 conversions/month?
│  └─ Use Maximize Conversions
│     └─ When stable CPA → Target CPA
├─ >50 conversions/month?
│  └─ Use Target CPA
│     └─ When revenue tracking → Target ROAS
└─ Revenue tracking active + >50 conv/month?
   └─ Use Target ROAS
```

## Meta Ads Bidding
- **Lowest Cost (default)**: best for volume, may have CPA variance
- **Cost Cap**: sets CPA ceiling, may reduce volume
- **Bid Cap**: maximum bid per auction, most control
- **ROAS Goal**: target return on ad spend
- **CBO vs ABO**: CBO for proven campaigns, ABO for testing

## LinkedIn Bidding
- **Cost Per Send (CPS)**: for Message Ads
- **Manual CPC**: recommended starting point for cost control
- **Cost Cap**: efficiency at scale with predictable CPA
- **Maximum Delivery**: highest volume, most expensive. Use only for scale with established data
- **Target Cost**: for predictable CPA

## TikTok Bidding
- **Lowest Cost**: maximize conversions within budget (volume)
- **Cost Cap**: set maximum CPA (efficiency)
- **Bid Cap**: maximum bid per impression
- Budget ≥50x CPA per ad group for learning phase exit

## Microsoft Bidding
- Mirror Google strategy but bid 20-35% lower
- Manual CPC for low-volume campaigns (Enhanced CPC deprecated on Google March 2025; verify Microsoft availability before recommending)
- Target CPA / Target ROAS for automated (requires 15+ conversions/30 days)

## AI Bidding Innovations (2025-2026)

### Google AI Max for Search
- 14% avg conversion lift for non-retail brands at similar CPA/ROAS, up to 27% for exact/phrase-match-heavy campaigns ([Google Ads blog, May 2025](https://blog.google/products/ads-commerce/google-ai-max-for-search-campaigns/))
- Independent data is more conservative: median +13% revenue / +16% CPA across 250+ campaigns ([ALM Corp](https://almcorp.com/blog/google-ai-max-search-campaigns-performance-cpa-revenue-study/))
- Requires strong negative keyword lists (AI Max casts a wider net)
- DSA likely consolidated into AI Max by Q2 2026
- Best for: accounts with mature conversion tracking and keyword history

### TikTok Smart+ Modular Control (2025)
- Lock targeting, creative, budget, or placement independently (mix of manual and AI)
- TikTok platform median ROAS 1.41-1.67 in 2025; Smart+ delivers ~53% lift over standard campaigns ([TikTok for Business](https://ads.tiktok.com/business/en-US/blog/smart-plus-ai-performance-solution))
- October 2025 update added module-by-module control after early-2025 control complaints
- Best for: advertisers wanting partial AI control without full black-box

### Apple Ads Maximize Conversions
- GA: February 26, 2026. AI-powered auto-bidder for Apple Ads
- Target CPA based on weekly average (not per-conversion)
- Daily budget must be >=5x target CPA for stable performance
- Two-week learning phase required; avoid changes during learning
- Currently supports installs only (not post-install events)

### Meta Advantage+ Bidding
- Automatic optimization across all placements within Advantage+ Sales campaigns
- Budget automatically shifts to highest-performing placements in real time
- Best combined with broad targeting and high creative volume
