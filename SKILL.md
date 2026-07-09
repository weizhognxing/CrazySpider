---
name: b2b-product-intelligence
description: Use when researching, crawling, scoring, or validating high-ticket, new, light-delivery B2B products, SaaS ideas, promotion channels, product intelligence, or information-arbitrage opportunities.
---

# B2B Product Intelligence

Use this skill to discover B2B products that match three criteria: high-ticket, newly launched or fast-emerging, and light-delivery. The goal is to continuously collect product and channel intelligence, identify information gaps, and turn the process into a repeatable methodology.

## Target Definition

Prioritize products with these traits:

- High-ticket: likely ACV, monthly price, or deal size is high enough to support meaningful B2B revenue.
- New product: recently launched, recently funded, recently trending, or recently gaining customer attention.
- Light-delivery: software-first, self-serve, API-based, template-based, or workflow-based; avoids heavy consulting, custom implementation, physical delivery, or long deployment cycles.
- B2B buyer: sells to companies, teams, operators, founders, marketers, sales teams, finance, HR, legal, supply chain, agencies, or developers.
- Replicable insight: product idea, positioning, channel, or go-to-market pattern can be analyzed and reused.

## Source Matrix

Start from sources that naturally expose new product, pricing, traction, or channel signals.

| Source Type | Example Sources | Crawl Or Extract |
| --- | --- | --- |
| New product discovery | Product Hunt, BetaList, Hacker News Show, Launching Next | launch date, product tagline, tags, website, votes, comments |
| Indie founders | Indie Hackers, X/Twitter build-in-public, founder blogs | MRR, launch notes, customer segment, pricing, channels |
| Funding signals | Crunchbase, ITjuzi, 36Kr, TechCrunch funding posts | funding date, category, market, target buyer, website |
| Software directories | G2, Capterra, SaaSworthy, AlternativeTo | category, pricing, review velocity, pain points, alternatives |
| Open-source commercialization | GitHub Trending, GitHub topics, npm packages | stars growth, new repositories, sponsor links, hosted products |
| Ad validation | Facebook Ad Library, Google Ads transparency, TikTok Creative Center | active ads, landing pages, copy angles, audience hints |
| Domain and website signals | new .com/.io/.ai domains, startup directories | new domains, pricing pages, signup flow, category keywords |

## Crawling Pipeline

Build a crawler workflow with this sequence:

1. Collect raw candidates from each source daily or weekly.
2. Normalize data into a common schema: `name`, `url`, `source`, `launch_date`, `description`, `tags`, `pricing_url`, `pricing_text`, `buyer`, `delivery_type`, `evidence`, `created_at`.
3. Fetch each candidate website, especially homepage, pricing page, docs page, changelog, case studies, and comparison pages.
4. Extract structured signals with rules first, then use an LLM for judgment and explanation.
5. Score candidates and store both raw evidence and final score.
6. Push the top candidates to a report, dashboard, CSV, Feishu/WeCom/Slack bot, or Git-tracked markdown file.

## Scoring Rubric

Score each candidate from 1 to 5 on each dimension.

| Dimension | Score 1 | Score 3 | Score 5 |
| --- | --- | --- | --- |
| High-ticket potential | free/consumer/low-price | $50-$200/mo or team pricing | $200+/mo, annual contract, enterprise, demo-led |
| Newness | mature crowded product | recent updates or recent attention | launched/funded/trending in last 90 days |
| Light delivery | consulting, hardware, custom project | onboarding required but repeatable | self-serve SaaS/API/template/workflow product |
| B2B fit | consumer or creator tool | prosumer/team tool | clear company buyer and business ROI |
| Channel signal | no visible acquisition channel | organic/community/search signs | active ads, SEO moat, marketplace, directory, partner channel |
| Information gap | obvious saturated idea | niche angle or weak competition | overlooked category with clear arbitrage potential |

Use this priority formula:

```text
priority_score = high_ticket * 0.25 + newness * 0.20 + light_delivery * 0.20 + b2b_fit * 0.15 + channel_signal * 0.10 + information_gap * 0.10
```

Shortlist candidates with `priority_score >= 4.0`. Keep `3.5-4.0` as watchlist items.

## High-Ticket Signals

Look for these machine-readable or LLM-detectable signals:

- Pricing contains `$199/mo`, `$299/mo`, `$499/mo`, `$999/mo`, annual plans, seat pricing, usage pricing, or minimum contracts.
- Website contains `Enterprise`, `Talk to Sales`, `Book a Demo`, `Request Demo`, `Contact Sales`, or `Custom Pricing`.
- Buyer language includes `sales teams`, `HR teams`, `finance teams`, `legal teams`, `operations`, `procurement`, `compliance`, `security`, `agencies`, or `developers`.
- Case studies mention recognizable companies, funded startups, departments, or measurable ROI.
- Product replaces expensive labor, agency work, compliance work, sales operations, data collection, or repetitive internal workflows.

## Light-Delivery Signals

Favor products with these traits:

- Signup, free trial, demo sandbox, API key, Chrome extension, Slack app, Shopify app, HubSpot app, Zapier integration, or template library.
- Documentation, onboarding checklist, public API docs, help center, changelog, and integration guides.
- Core value is software automation, data enrichment, AI workflow, monitoring, reporting, scraping, matching, routing, alerting, or content transformation.

Avoid products with these signals unless there is a clear reason:

- `Implementation Fee`, `Professional Services`, `custom deployment`, `on-premise only`, `hardware`, `field service`, `agency service`, `done-for-you`, or heavy migration language.
- Complex procurement or regulated deployment where the product cannot be delivered repeatedly with low marginal effort.

## Newness Signals

Treat a product as new or emerging when at least one is true:

- Product was launched or submitted in the last 90 days.
- Website changelog, blog, or release notes show recent rapid iteration.
- GitHub stars, Product Hunt votes, reviews, or social mentions show recent acceleration.
- New funding, new team hiring, new paid ads, or new directory listings appeared recently.
- Category is connected to a recent platform shift, policy change, API launch, AI model capability, marketplace change, or regulation.

## Recommended MVP

Start with a minimal crawler stack before expanding sources:

1. Product Hunt daily launches: collect product names, descriptions, topics, websites, votes, and comments.
2. G2 or Capterra category pages: collect recently reviewed tools and pain points from reviews.
3. Indie Hackers or founder posts: collect revenue-transparent products and launch stories.
4. Product websites: crawl homepage, pricing page, docs, changelog, case studies, and integrations.
5. LLM scorer: return `scores`, `evidence`, `why_it_matters`, `possible_channel`, and `replication_angle`.

## Output Format

For each candidate, produce a compact record:

```json
{
  "name": "Product Name",
  "url": "https://example.com",
  "source": "Product Hunt",
  "category": "B2B SaaS",
  "buyer": "Sales teams",
  "pricing_signal": "$299/mo and Enterprise plan",
  "delivery_signal": "self-serve SaaS with API docs",
  "newness_signal": "launched this month",
  "channel_signal": "active SEO pages and comparison pages",
  "scores": {
    "high_ticket": 5,
    "newness": 5,
    "light_delivery": 4,
    "b2b_fit": 5,
    "channel_signal": 4,
    "information_gap": 4
  },
  "priority_score": 4.6,
  "why_it_matters": "Clear B2B pain, high willingness to pay, and self-serve delivery.",
  "replication_angle": "Could build a niche-specific version for agencies or vertical teams."
}
```

## Daily Report Template

Use this structure for a daily or weekly intelligence report:

```markdown
# B2B Product Intelligence Report

## Top Candidates

| Rank | Product | Buyer | Signal | Score | Replication Angle |
| --- | --- | --- | --- | --- | --- |

## Best Channel Signals

Summarize which channels appear to be working: SEO, ads, communities, directories, partnerships, marketplaces, outbound, influencer, or open source.

## Methodology Notes

Record which source produced useful leads, which filters failed, and which scoring rules need adjustment.

## Watchlist

List promising but incomplete candidates requiring follow-up.
```

## Implementation Guidance

When implementing this in code:

- Use Scrapy for stable static pages and Playwright for JS-heavy websites.
- Store raw HTML snapshots or extracted text to support later review.
- Deduplicate by normalized domain and canonical URL.
- Keep source-specific crawlers small; use a shared normalization and scoring layer.
- Add polite rate limits and obey robots.txt where applicable.
- Do not store secrets in code; use environment variables for APIs and webhook URLs.
- Log extraction failures and keep raw candidates even if scoring fails.

## LLM Scoring Prompt

Use this prompt when scoring a candidate:

```text
You are evaluating a B2B product opportunity for information-arbitrage research.

Criteria:
1. High-ticket potential: 1-5
2. Newness: 1-5
3. Light-delivery fit: 1-5
4. B2B fit: 1-5
5. Channel signal: 1-5
6. Information gap: 1-5

Return valid JSON only. Include short evidence for every score. Penalize consumer products, low-priced tools, heavy consulting, hardware, and products requiring custom implementation.

Input:
{{candidate_text}}
```

## Success Criteria

The workflow is successful when it regularly produces:

- 5-10 credible weekly candidates with clear evidence.
- At least one repeatable source that produces high-quality leads.
- A growing library of product categories, price signals, and channel patterns.
- A shortlist of ideas suitable for fast validation, landing page tests, scraping prototypes, or outbound experiments.
