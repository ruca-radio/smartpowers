# campaign-brief.md Format Specification

Reference for `smartpowers:ads-create`. The following section headings are a
**parsing contract**; agents downstream depend on these exact heading names.

```markdown
# Campaign Brief: [brand_name]
**Generated:** [date]
**Website:** [website_url]
**Platforms:** [comma-separated list]
**Objective:** [objective]
**Concepts:** [N]

## Brand DNA Summary
[3-sentence synthesis of brand-profile.json: voice, visual identity, target audience]

## Audit Context
[If audit data found: top 3 weaknesses being addressed]
[If no audit data: "No audit data; run an ads audit for weakness-targeted concepts"]

## Campaign Concepts

### Concept 1: [Name]
**Hypothesis:** [why this will work; 1 sentence]
**Primary Message:** [core message; 1 sentence]
**Tone:** [voice reading from brand-profile.json]
**Visual Direction:** [2-3 sentences describing imagery]
**Target Platforms:** [platforms and rationale]
**CTA:** [call to action text]
**Addresses:** [audit finding or "general brand awareness"]

### Concept 2: [Name]
[same structure]

[repeat for all concepts]

## Copy Deck
[appended by copy-writer agent; headlines, primary text, CTAs per concept per platform]

## Image Generation Briefs

### Brief 1: [Concept Name]: [Platform]
**Prompt:** [exact generation prompt]
**Dimensions:** [WxH]
**Safe zone notes:** [constraint or "None"]

### Brief 2: [Concept Name]: [Platform]
**Prompt:** [exact generation prompt]
**Dimensions:** [WxH]
**Safe zone notes:** [constraint or "None"]

[one brief per concept × platform combination]

## Next Steps
1. Review all concepts and select which to move forward with
2. Generate images from the briefs above
3. Adjust CTAs and offers in the copy deck for your specific promotion
4. Upload final assets to your ad platform managers
```
