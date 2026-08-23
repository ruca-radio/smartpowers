---
name: ads-create
description: Use when the user asks to create a campaign, campaign brief, ad concepts, ad copy, campaign strategy, ad messaging, creative brief, or generate concepts. Produces structured campaign concepts, messaging pillars, and platform-specific copy decks from a brand profile; outputs a campaign-brief markdown file.
---

# Ads Create: Campaign Concept & Copy Brief Generator

Generates structured campaign concepts and platform-specific copy from your
brand profile and optional audit data. Outputs campaign-brief.md — the
handoff artifact for any downstream asset-generation step.

Listen to the brand voice before typing; every headline and CTA must carry
emotional resonance. Create the deliverable — do not hedge concepts so
heavily that the next person has to do the work. Spec compliance without
emotional pull is a fail.

## Process

### Step 1: Check for Brand Profile

Look for brand-profile.json in the current directory.

- **Found**: Load and proceed.
- **Not found**: Ask the user — run a brand-DNA extraction step first if one
  is available in your suite, or describe the brand manually and build a
  basic profile from the description.

If the user chooses manual, collect:
- Brand name and website
- Primary color (or "unsure")
- 3 words that describe the brand voice
- Target audience (age, role, key pain point)
- Main product/service offering

### Step 2: Check for Audit Results

Look for ADS-AUDIT-REPORT.md or any *-audit-results.md in the current directory.

- **Found**: Read them. Note the top 3 weaknesses (creative fatigue, tracking gaps, wasted spend) to address in concepts.
- **Not found**: Continue without. Note in the brief: "No audit data found; concepts are generalized. Run an ads audit for weakness-targeted concepts."

### Step 3: Collect Campaign Parameters

If the user's request already specifies platforms or objective (e.g. flags
like `--platforms meta google` or `--objective leads`), use those values and
skip the corresponding questions below.

Ask (combine into one message; omit anything already provided):
1. **Platforms**: Which ad platforms? (Meta · Google · LinkedIn · TikTok · YouTube · Microsoft · All)
2. **Objective**: Sales/Revenue · Leads/Demos · App Installs · Brand Awareness · Retargeting
3. **Offer or brief**: Any specific offer, promotion, or message to highlight? (optional)
4. **Number of concepts**: How many campaign concepts? (default: 3)

### Step 4: Select Copy Framework

Read `references/copy-frameworks.md` and recommend a framework based on
campaign goal + platform + audience temperature. Include the selected
framework name in the brief for the copy-writer agent.

### Step 5: Spawn Creative Agents in Sequence

Agents must run **sequentially**; the copy-writer reads the file the
creative-strategist writes, so running them in parallel races on
campaign-brief.md. This is a stage gate per
`smartpowers:orchestrating-agent-swarms` — wait for each agent to fully
complete before dispatching the next.

**Step 5a: Spawn the creative-strategist.**
It creates campaign-brief.md and writes the strategic sections:
"Brand DNA Summary", "Campaign Concepts", "Image Generation Briefs",
"Next Steps" (exact heading contract in `references/brief-format.md`).

Additional instructions:
- For e-commerce businesses, apply an e-commerce creative playbook
  (Product Launch, Sale/Promotion, Seasonal, Retargeting, Brand Awareness)
  if one is available in your suite
- Include banana domain mode recommendations in each Image Generation Brief
  (Product, Editorial, Cinema, UI/Web, or Portrait)

**Step 5b: Spawn the copy-writer.**
After the creative-strategist completes, the copy-writer reads the existing
campaign-brief.md and appends the "Copy Deck" section with platform-specific
headlines, primary text, and CTAs.

Additional instructions:
- Apply the selected framework structure from `references/copy-frameworks.md` to all ad copy
- Generate 2 framework variants per platform: primary (recommended framework) + secondary (alternative for A/B testing)

### Step 6: Review and Present

After both agents complete, confirm campaign-brief.md exists and is complete.

Present a summary to the user:
```
✓ campaign-brief.md generated

Summary:
  Concepts: [N] campaign concepts created
  Platforms: [list]
  Copy deck: Headlines, primary text, and CTAs for each concept × platform
  Image briefs: [N] image generation briefs ready

Next steps:
  1. Review campaign-brief.md and adjust any messaging
  2. Generate images from the briefs
  3. Upload copy and assets to your ad platforms
```

## Brief Format

The exact heading structure of campaign-brief.md is a **parsing contract** —
downstream agents depend on it. Full specification in
`references/brief-format.md`.

## Quality Gates

- **Minimum 3 concepts** (unless user requests fewer)
- **Distinct angles**: no two concepts share the same primary message angle
- **Platform fit**: concepts targeting TikTok must acknowledge vertical-only format and sound-on context
- **Offer anchoring**: if the user provided a specific offer, at least 1 concept must lead with it
- **Image briefs**: every concept must have at least one image brief per requested platform

## Meta Andromeda Optimization

For Meta campaigns: recommend diverse creative concepts (different motivators, visual styles, messaging angles) to maximize Andromeda retrieval. Similarity Score >60% between ads triggers clustering and suppression.

## Platform Character Limits

Verify platform character limits are current. Meta reduced headline display length on mobile in 2025.
