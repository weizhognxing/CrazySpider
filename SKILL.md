---
name: paid-traffic-product-collector
description: Use when collecting, crawling, filtering, and scoring products suitable for paid-traffic arbitrage, especially high-ticket, newly launched, non-ecommerce, B2B online software products with identifiable business customers and low trial friction.
---

# Paid Traffic Product Collector

This skill is for collecting products that may be suitable for making money through paid traffic. The workflow has two layers: hard filters and scoring. The user's standards are hard filters. If a candidate does not pass them, remove it directly. Additional standards are only scoring bonuses.

## Core Goal

Find products with these properties:

- They can be acquired through paid ads or paid traffic.
- They have enough gross profit or lifetime value to cover ad cost.
- They target identifiable business customers.
- They can be delivered mostly online with low marginal cost.
- They have a clear low-risk first action, such as trial, demo, diagnostic report, ROI calculator, pilot, or low-cost first order.

## Hard Filters

Apply these first. If any item clearly fails, reject the product and do not score it.

| Filter | Required Standard | Reject If |
| --- | --- | --- |
| High-ticket potential | Product has medium/high order value, enterprise pricing, annual plan, seat pricing, usage pricing, or clear upsell path | Only low-price consumer purchase or one-time small order |
| Newly launched or emerging | Product is recently launched, recently funded, recently promoted, newly trending, or in a newly emerging category | Mature saturated product with no new angle or recent signal |
| Non-ecommerce | Product is not a normal physical goods ecommerce item | Depends on inventory, logistics, warehousing, returns, or price-war retail |
| B2B orientation | Product sells to companies, teams, departments, shops, agencies, schools, clinics, factories, or business operators | Mainly consumer entertainment, lifestyle, personal shopping, or pure C-end app |
| Customer list can be built | Target customers can be found through Qichacha, Tianyancha, maps, job sites, industry directories, company websites, app stores, marketplaces, or public databases | Cannot define or locate target customers in bulk |
| Online software or light online service | Product is software, data, automation, AI workflow, SaaS, API, plugin, template, dashboard, online tool, or standardized digital service | Requires heavy offline delivery, custom projects, hardware installation, field service, or manual agency work for each customer |
| Low trial friction | Has free trial, demo, sandbox, free diagnosis, ROI report, pilot, low-cost first order, money-back guarantee, or result-based entry point | Customer must pay a large amount before seeing any proof |

## Hard Filter Decision Output

For every collected candidate, return one of these statuses:

- `accepted`: passes all hard filters and should be scored.
- `rejected`: fails one or more hard filters.
- `uncertain`: not enough information; keep in watchlist and collect more evidence.

Always include the rejection reason if rejected.

## Scoring Standards

Only score candidates that pass the hard filters. Score each item from 1 to 5. These standards are bonuses and ranking signals, not mandatory filters.

| Scoring Dimension | Score 1 | Score 3 | Score 5 |
| --- | --- | --- | --- |
| Pain intensity | Nice-to-have | Solves a real workflow problem | Solves urgent loss, revenue, compliance, hiring, sales, or cost problem |
| ROI clarity | Value is vague | Some efficiency value can be explained | ROI can be calculated as revenue gained, cost saved, risk reduced, or time saved |
| Gross margin | Human-heavy or low margin | Mixed software and service | Mostly software/data/automation with high margin |
| Sales cycle | Long approval or procurement | Some sales follow-up needed | Can convert in days or weeks through trial, demo, pilot, or founder/manager decision |
| Decision maker clarity | Buyer unclear | Team user known but payer unclear | Clear owner, founder, department head, marketer, HR, finance, sales, legal, or operations buyer |
| Ad message clarity | Needs long education | Can explain in a landing page | Can explain in one ad hook: who it helps, what pain it solves, what result it creates |
| Trust assets | No proof | Some screenshots or testimonials | Has case studies, customer logos, review data, before/after results, certification, or public traction |
| Retention potential | One-time use | Occasional repeat use | Monthly/annual recurring use with data, workflow, collaboration, or reporting lock-in |
| Expansion potential | Single user only | Can add features | Can expand by seats, branches, stores, usage, modules, departments, or enterprise plan |
| Delivery standardization | Mostly manual | Repeatable onboarding | Self-serve, template-based, API-based, automated, or standardized setup |
| Migration cost | Requires major change | Needs some setup | Can run alongside current process or import data easily |
| Channel evidence | No visible channel | Organic/community/search evidence | Competitors or product itself show active ads, SEO pages, directories, affiliate, partner, marketplace, or outbound potential |
| Competition entry window | Overcrowded red ocean | Demand exists but positioning differs | Verified demand with weak incumbents, new regulation/platform change, or underserved niche |
| Compliance safety | Risky claims/data/category | Manageable risk | Platform-ad-friendly, legal, privacy-safe, and low policy risk |

## Weighted Score

Use this formula after scoring:

```text
traffic_fit_score =
  pain_intensity * 0.13 +
  roi_clarity * 0.12 +
  gross_margin * 0.10 +
  sales_cycle * 0.09 +
  decision_maker_clarity * 0.08 +
  ad_message_clarity * 0.08 +
  trust_assets * 0.07 +
  retention_potential * 0.08 +
  expansion_potential * 0.07 +
  delivery_standardization * 0.07 +
  migration_cost * 0.04 +
  channel_evidence * 0.04 +
  competition_entry_window * 0.02 +
  compliance_safety * 0.01
```

Ranking interpretation:

- `4.3-5.0`: strong candidate, prioritize manual validation.
- `3.8-4.29`: good candidate, keep and collect more proof.
- `3.3-3.79`: watchlist, only keep if source is unique or evidence is incomplete.
- `<3.3`: deprioritize.

## Collection Sources

Use sources that expose newness, pricing, buyer, channel, or traction signals.

| Source Type | Example Sources | Extracted Signals |
| --- | --- | --- |
| New product platforms | Product Hunt, BetaList, Hacker News Show, Launching Next | launch date, tagline, tags, comments, votes, website |
| SaaS directories | G2, Capterra, SaaSworthy, AlternativeTo | category, pricing, reviews, competitors, pain points |
| Founder communities | Indie Hackers, X/Twitter build-in-public, founder blogs | MRR, launch story, buyer, channel, experiments |
| Funding/news | Crunchbase, TechCrunch, 36Kr, ITjuzi | new funding, industry, buyer, product category |
| Ad libraries | Facebook Ad Library, Google Ads Transparency, TikTok Creative Center | active ads, landing pages, hooks, creative angles |
| Open-source and developer ecosystems | GitHub Trending, GitHub topics, npm, Chrome Web Store, Shopify App Store, HubSpot App Marketplace | adoption, integration, marketplace demand |
| Business customer databases | Qichacha, Tianyancha, Amap/Baidu Maps, job boards, industry associations | customer count, industry density, decision makers, company size |
| Search and SEO | Google/Bing/Baidu SERP, comparison pages, alternative pages | demand keywords, competitor positioning, paid/organic competition |

## China Data Sources

For the China-first MVP, prioritize domestic sources because they are easier to access from a domestic network and map directly to customer discovery, paid-traffic validation, and B2B software discovery.

| Priority | Source | Use Case | Signals To Extract |
| --- | --- | --- | --- |
| P0 | Feishu App Directory | Find B2B online software and workplace plugins | app category, target users, install flow, trial/demo, screenshots, vendor, update recency |
| P0 | DingTalk App Market | Find enterprise SaaS and light-delivery workflow tools | category, buyer, pricing hints, reviews, deployments, vendor profile |
| P0 | WeCom service provider/app ecosystem | Find enterprise WeChat tools, SCRM, customer service, marketing, HR, approval workflows | product type, target company, service provider, implementation level, customer cases |
| P0 | Qichacha / Tianyancha / AiQicha | Validate whether target customers can be found in bulk | company count, industry, region, business scope, company size, decision-maker clues |
| P0 | Baidu / 360 / Sogou search | Find product websites, landing pages, competitors, paid search traces | keyword demand, landing pages, competitor messages, ads, SEO pages |
| P0 | Ocean Engine / Juying / 巨量创意 / 巨量算数 | Validate paid-traffic feasibility and creative angles | active creatives, hooks, landing pages, audience angles, industry ad volume |
| P0 | Kuaishou Magnetic Engine / 磁力引擎 | Validate short-video ad demand and creative patterns | ad creatives, selling points, landing pages, target audience |
| P0 | WeChat Search / Official Accounts | Find new SaaS, service providers, case studies, product launches, industry articles | launch articles, customer cases, pain points, founder/company narrative |
| P0 | 36Kr / Chuangyebang / ITjuzi | Find new companies, new funding, new B2B products, emerging categories | funding date, product category, team, buyer, market timing |
| P1 | 5118 / Aizhan / Chinaz / Baidu Index | Validate search demand and keyword competitiveness | search volume, related keywords, competitor domains, trend, CPC clues |
| P1 | Alibaba Cloud Marketplace / Tencent Cloud Marketplace / Huawei Cloud Marketplace | Find enterprise software, SaaS, security, data, AI, industry solutions | product category, pricing, vendor, deployment type, customer reviews, cloud integration |
| P1 | Boss Zhipin / Lagou / Liepin | Infer business pain from hiring demand | hiring category, role pain, company type, budget signal, urgent operational needs |
| P1 | Xiaohongshu / Douyin / Video Channels | Observe service providers, tool promotions, and ad-like content | hooks, comments, pain points, service packaging, creator distribution |
| P2 | Zhihu / Juejin / CSDN | Validate developer tools, AI tools, data tools, and technical pain points | discussions, alternatives, adoption barriers, developer demand |
| P2 | 人人都是产品经理 / 鸟哥笔记 / 梅花网 | Track marketing, operations, private-domain, and growth tool trends | product trends, channel strategies, conversion methods, user pain points |

## China-First Source Strategy

Use the domestic data sources in this order:

1. Product discovery: Feishu, DingTalk, WeCom, cloud marketplaces, 36Kr, Chuangyebang, ITjuzi.
2. Website verification: official site, pricing page, demo/trial page, help docs, customer cases, update logs.
3. Paid-traffic validation: Ocean Engine, 巨量创意, 巨量算数, 磁力引擎, Baidu search ads, Douyin/Xiaohongshu content.
4. Customer-list validation: Qichacha, Tianyancha, AiQicha, Amap/Baidu Maps, job boards, industry directories.
5. Demand validation: Baidu Index, 5118, Chinaz, Aizhan, WeChat Search, Zhihu, CSDN.

The preferred China-first crawl chain is:

```text
Feishu / DingTalk / WeCom / Cloud Marketplace
  -> official website / pricing / trial / docs / case studies
  -> Ocean Engine / Baidu / Douyin / WeChat search for paid-traffic evidence
  -> Qichacha / Tianyancha / maps / job boards for customer-list evidence
  -> hard filters
  -> scoring
  -> candidate table
```

## China MVP Scope

Start with only five source groups before expanding:

| Step | Source Group | Why It Comes First |
| --- | --- | --- |
| 1 | Feishu / DingTalk / WeCom app ecosystems | They are naturally B2B, online, software-like, and often light-delivery |
| 2 | Product official websites | Pricing, trial, demo, docs, delivery model, and cases are usually found here |
| 3 | Ocean Engine / 巨量创意 / Baidu search | They reveal whether similar offers can be advertised and how hooks are written |
| 4 | Qichacha / Tianyancha / AiQicha / maps | They validate whether target customers can be collected in bulk |
| 5 | 36Kr / ITjuzi / Chuangyebang | They provide newness, funding, and emerging-category signals |

## Domestic Product Categories To Watch

These categories often fit the hard filters and are good starting points for domestic collection. Still apply the hard filters before scoring.

| Category | Why It Fits The Search |
| --- | --- |
| AI customer service / intelligent customer service | B2B, ROI is easy to explain, online delivery, clear buyer |
| Sales leads / CRM / SCRM | Customer list can often be built from company databases; revenue value is clear |
| Recruitment / HR efficiency tools | Hiring pain can be validated through job boards; clear HR or founder buyer |
| Finance / tax / invoice / compliance tools | Strong recurring need and clear risk-reduction value |
| Corporate training / employee exam systems | Customers can be segmented by industry and company size; delivery can be online |
| Contract / legal / e-signature tools | Risk reduction and workflow efficiency are clear |
| Data collection / business intelligence / opportunity monitoring | Fits information-arbitrage logic and has clear B2B use cases |
| Store management / private-domain operations | Offline merchants can be found through maps and business databases |
| WeCom / DingTalk / Feishu plugins | Platform trust, light delivery, and clear installation path |
| Vertical industry SaaS | Narrow customer segment, clearer targeting, less competition if niche is underserved |

## Product Evidence To Collect

For every candidate, collect these fields when possible:

- `name`
- `website`
- `source`
- `launch_or_newness_signal`
- `category`
- `target_customer`
- `decision_maker`
- `pricing_signal`
- `trial_or_low_risk_entry`
- `delivery_model`
- `customer_list_source`
- `ad_message_hook`
- `roi_claim`
- `trust_assets`
- `competitors`
- `channel_signal`
- `hard_filter_status`
- `hard_filter_reasons`
- `traffic_fit_score`
- `next_validation_step`

## Recommended Workflow

Follow this sequence:

1. Collect raw products from source pages or APIs.
2. Visit each candidate's homepage, pricing page, docs, demo/trial page, case studies, integrations, and blog/changelog.
3. Apply hard filters using evidence. Reject obvious failures immediately.
4. Score accepted candidates using the scoring standards.
5. Deduplicate by domain and product name.
6. Output accepted candidates, rejected candidates, and uncertain watchlist separately.
7. For top candidates, propose the next validation step: scrape customer list, build ad hook, inspect competitors' ads, estimate CAC/LTV, or test a landing page.

## Output Format

Use this table for human-readable reports:

| Product | Status | Score | Target Customer | Pricing Signal | Low-Risk Entry | Customer List Source | Ad Hook | Key Reason | Next Step |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |

Use this JSON for machine-readable storage:

```json
{
  "name": "Product Name",
  "website": "https://example.com",
  "source": "Product Hunt",
  "hard_filter_status": "accepted",
  "hard_filter_reasons": {
    "high_ticket_potential": "Enterprise plan and $299/mo team plan",
    "newly_launched_or_emerging": "Launched within 60 days",
    "non_ecommerce": "SaaS software, no physical delivery",
    "b2b_orientation": "Targets sales teams",
    "customer_list_can_be_built": "Target companies can be found via Qichacha and job postings",
    "online_software_or_light_service": "Web app with API",
    "low_trial_friction": "Free trial and demo sandbox"
  },
  "scores": {
    "pain_intensity": 5,
    "roi_clarity": 5,
    "gross_margin": 5,
    "sales_cycle": 4,
    "decision_maker_clarity": 4,
    "ad_message_clarity": 5,
    "trust_assets": 3,
    "retention_potential": 4,
    "expansion_potential": 4,
    "delivery_standardization": 5,
    "migration_cost": 4,
    "channel_evidence": 3,
    "competition_entry_window": 4,
    "compliance_safety": 5
  },
  "traffic_fit_score": 4.48,
  "ad_message_hook": "Find missed sales leads automatically from company signals.",
  "next_validation_step": "Check competitor ad libraries and estimate available customer count."
}
```

## Rejection Examples

Reject with clear reasons:

```json
{
  "name": "Candidate",
  "hard_filter_status": "rejected",
  "rejection_reasons": [
    "Fails non-ecommerce filter: physical product with inventory and returns",
    "Fails customer-list filter: target buyer cannot be found or segmented in bulk"
  ]
}
```

## LLM Evaluation Prompt

Use this prompt to evaluate a product candidate:

```text
You are evaluating whether a product is suitable for making money through paid traffic.

Important rule: the user's standards are hard filters. If the product fails any hard filter, reject it directly and do not score it.

Hard filters:
1. High-ticket potential
2. Newly launched or emerging
3. Non-ecommerce
4. B2B orientation
5. Customer list can be built through public/company databases
6. Online software or light online service
7. Low trial friction through trial, demo, diagnosis, ROI report, pilot, low-cost first order, guarantee, or result-based entry

If accepted, score these dimensions from 1 to 5:
pain_intensity, roi_clarity, gross_margin, sales_cycle, decision_maker_clarity, ad_message_clarity, trust_assets, retention_potential, expansion_potential, delivery_standardization, migration_cost, channel_evidence, competition_entry_window, compliance_safety.

Return valid JSON only. Include evidence for every hard filter and every score. Do not list unrelated products.

Candidate text:
{{candidate_text}}
```

## Final Principle

Do not collect broad product lists. Collect only products that pass the user's hard filters. Use scoring only to rank the survivors.
