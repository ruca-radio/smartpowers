---
name: ads-competitor
description: Use when the user asks for competitor ads, ad spy, competitive analysis, competitor PPC, ad intelligence, Meta Ad Library, Facebook Ad Library, Google Ads Transparency Center, competitor creative, or competitor research. Analyzes competitor copy, creative, keyword targeting, and estimated spend; identifies competitive gaps and opportunities.
---

# Competitor Ad Intelligence

## Process

1. Identify target competitors (from user input or industry analysis)
2. Establish industry CPC/CTR/CVR baselines (from benchmark references if available)
3. Research competitor ad presence across platforms
4. Analyze ad copy, creative, and messaging themes
5. Estimate competitor spend and keyword strategy
   (manual estimation formulas in `references/response-playbook.md`)
6. Identify gaps and opportunities
7. Generate competitive intelligence report

Check `references/platform-updates.md` first — platform capabilities shift
fast (Meta Andromeda, Google AI Max, Demand Gen, TikTok Symphony), and stale
assumptions produce stale analysis.

## Data Sources

### Free Intelligence Sources
| Source | Platform | What You Can Find |
|--------|----------|------------------|
| Google Ads Transparency Center | Google | Active ads, formats, geo targeting |
| Meta Ad Library | Meta/Instagram | All active ads, creative, copy, spend range |
| LinkedIn Ad Library | LinkedIn | Active ads from company pages |
| TikTok Creative Center | TikTok | Top ads, trending creative, hashtags |
| Microsoft Ads | Microsoft | Limited: use auction insights |
| Apple Ads (App Store) | Apple | Search tab ads, Today tab ads, product page creatives |

### Google Ads Auction Insights
Available from the user's own Google Ads account:
- Impression share vs competitors
- Overlap rate (how often you compete)
- Outranking share (who wins more often)
- Top of page rate and absolute top of page rate
- Available for Search and Shopping campaigns

### Platform-Specific Research

Per-platform research tactics (Google, Meta, LinkedIn, TikTok, Apple Ads)
live in `references/platform-sources.md`.

## Competitive Analysis Framework

### 1. Ad Copy Analysis
For each competitor, document:
- **Headlines**: primary messages and value propositions
- **CTAs**: what action they're driving (free trial, demo, buy now, learn more)
- **Offers**: pricing, discounts, free shipping, trials
- **Tone**: professional, casual, urgent, educational, emotional
- **USPs**: unique selling propositions they emphasize
- **Pain points**: customer problems they address

### 2. Creative Strategy Analysis
- **Formats used**: image, video, carousel, collection, document
- **Visual style**: photography, illustration, UGC, stock, branded
- **Video approach**: studio quality vs UGC vs animated
- **Creative volume**: how many active ads (indicator of testing velocity)
- **Refresh frequency**: how often new creatives appear
- **Conceptual diversity**: Meta's Andromeda suppresses ads with >60%
  similarity — assess genuine diversity, not just volume

### 3. Messaging Themes
Categorize competitor messaging into themes:
| Theme | Competitor A | Competitor B | Your Brand |
|-------|-------------|-------------|------------|
| Price/Value | ✅ Primary | ⚠️ Secondary | ? |
| Quality/Premium | ❌ | ✅ Primary | ? |
| Speed/Convenience | ⚠️ Secondary | ❌ | ? |
| Trust/Authority | ✅ Primary | ✅ Primary | ? |
| Innovation | ❌ | ⚠️ Secondary | ? |

### 4. Keyword Intelligence (Google/Microsoft/Apple Ads)
- Brand keyword bidding: are competitors bidding on your brand?
- Keyword overlap: which non-brand terms do you both target?
- Keyword gaps: terms competitors rank for that you don't target
- Match type strategy: estimated match types from ad triggers

## Gap & Opportunity Identification

### Platform Gaps
- Which platforms are competitors NOT on? (opportunity to own)
- Which platforms are they underspending on? (opportunity to outspend)

### Messaging Gaps
- What customer pain points are NO competitors addressing?
- What value propositions are underrepresented in the market?
- What content formats are competitors not using?

### Audience Gaps
- What demographics/segments are competitors not targeting?
- What geographic markets are underserved?
- What funnel stages are competitors neglecting?

### Creative Gaps
- What ad formats are competitors not using? (video, UGC, Spark Ads)
- What creative styles are missing from the competitive landscape?
- What platform-specific features are competitors not leveraging?

## Competitive Response

Playbooks for when competitors bid on your brand and when you're outspent
live in `references/response-playbook.md`.

## Output

### Deliverables
- `COMPETITOR-INTELLIGENCE-REPORT.md`: Full competitive analysis
  - Per-competitor ad presence summary
  - Ad copy and messaging analysis
  - Creative strategy comparison
  - Estimated spend levels
  - Keyword overlap and gaps
- `COMPETITIVE-GAPS.md`: Opportunities identified from competitor analysis
  - Platform gaps
  - Messaging opportunities
  - Audience segments to target
  - Creative format opportunities
- Strategic recommendations for competitive positioning
- Priority actions to gain competitive advantage
