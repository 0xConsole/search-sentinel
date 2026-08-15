# SearchSentinel — Real-Time Search Intelligence & Anomaly Detection Agent

## Hackathon Summary

| Field | Value |
|-------|-------|
| Name | DevNetwork [API + Cloud + AI] Hackathon 2026 |
| URL | https://api-cloud-ai-hackathon-2026.devpost.com/ |
| Deadline | Sep 3, 2026 |
| Prize | $45,500 total across sponsor tracks |
| Participants | 595+ |
| Format | In-person (Santa Clara) + Online (online participation allowed) |
| Submission opens | Aug 17, 2026 |

## Target Sponsor Track: SerpApi — "Best AI Use Case using SerpApi search data"

- **Prize:** $1,000 cash + $1,000 SerpApi credits
- **Requirement:** "An innovative AI application using SerpApi APIs to access reliable, structured, real-time web data."
- **Judging criteria:** Progress, Concept, Feasibility

## The Problem

Search is the world's largest real-time signal of what people care about. Volatility in search
results — sudden ranking shifts, volume spikes, or unexpected queries appearing — is an early
indicator of breaking news, viral events, brand crises, algorithm updates, and emerging trends.
But nobody is watching continuously, because doing it manually is impossible and existing tools
(SQLO platforms, Google Trends dashboards) only show aggregates, not *anomalies with context*.

Marketers, brand teams, and trend-watchers need an **autonomous agent** that:

1. Continuously polls live search results via SerpApi
2. Detects **statistical anomalies** in rankings, result composition, and query volume
3. Correlates anomalies across related queries (a SERP shake-up in one query often signals an
   algorithm update that affects many)
4. Generates **automated intelligence reports** so a human never has to stare at a dashboard

This is the gap SearchSentinel closes.

## What SearchSentinel Does

SearchSentinel is an **autonomous AI agent** that uses SerpApi to monitor the live web and flag
search anomalies before they show up in any lagging dashboard. It exposes its entire capability
surface as **MCP-compatible tools** so it can be orchestrated by any AI agent, not just used as a
standalone web app.

### Core capabilities

- **Live SERP monitoring** — Pull current Google/Bing/News/YouTube search results for any query
  via SerpApi, extract organic results, answer boxes, related searches, and People Also Ask.
- **Anomaly detection** — Statistical detection of ranking volatility (z-score over rank positions),
  result-set churn (Jaccard distance vs baseline), and volume proxies (result count,
  related-query appearance). No ML training required — uses proven statistical methods so it
  works on day one without historical data.
- **Trend correlation** — When multiple tracked queries show simultaneous anomalies, flag a
  probable algorithm update or industry-wide event.
- **Auto-report generation** — Produces a structured intelligence report: anomalies found,
  severity, affected queries, evidence (real URLs + snippets from SerpApi), and recommendations.

### The 6+ MCP tools (agent-callable)

1. `serp_monitor` — Pull live SERP for a query (organic, news, answer box, related, PAA)
2. `track_rankings` — Track a query's top-10 ranking positions over time
3. `detect_ranking_anomalies` — Z-score based detection of ranking volatility
4. `detect_result_set_churn` — Jaccard distance vs baseline (new/disappeared results)
5. `detect_volume_anomalies` — Anomalies in result-count / related-query volume proxies
6. `correlate_anomalies` — Cross-query correlation to detect algorithm-update-scale events
7. `generate_intelligence_report` — Auto-generate a full Markdown/JSON intelligence report
8. `list_tracking_queries` — Inventory of tracked queries + their current anomaly scores

That's **8 tools** — exceeds the 6+ requirement and gives genuine agent capability.

## Why This Wins the SerpApi Track

1. **Direct fit to the stated requirement.** "Innovative AI application using SerpApi APIs to access
   reliable, structured, real-time web data" — SearchSentinel is built *entirely* on SerpApi as the
   primary data source, not a bolt-on.
2. **Anomaly detection is an underexplored SerpApi use case.** Most SerpApi hackathon entries build
   SEO dashboards, price trackers, or chat-with-search demos. Statistical anomaly detection on
   live SERPs is novel and defensible.
3. **Agent-native, MCP-compatible.** Judges increasingly reward agent patterns; exposing every
   capability as an MCP tool makes SearchSentinel composable into larger agent workflows (not a
   dead-end web app).
4. **Works on day one, demo-mode friendly.** Statistical anomaly detection needs no training data;
   demo mode ships with realistic mock SERPs so judges can exercise every tool without a SerpApi
   key. Live mode is one env var (`SERPAPI_API_KEY`) away.
5. **Real feasibility.** Search monitoring as a SaaS is a proven market (Ahrefs, Semrush,
   Sistrix). SearchSentinel is a credible MVP for an "anomaly-first" position in that market.

## Differentiation from Prior Builds

This is a **distinct project** from our earlier SerpApi-track entry (SerpShield, threat
intelligence). SearchSentinel's focus is **search trend & ranking anomaly detection** — a
marketing/intelligence use case, not security. The two entries are complementary, not duplicate:
- SerpShield = "what's the web saying about my brand that could hurt me?" (security)
- SearchSentinel = "what just changed in the search results, and is it an anomaly?" (intelligence)

Both are legitimate, non-overlapping SerpApi use cases; entering both maximizes track coverage.

## Architecture

```
search-sentinel/
├── api/index.py          # Vercel serverless entry → FastAPI app
├── app/
│   ├── main.py           # FastAPI app, routes, MCP endpoint, demo endpoint
│   ├── agent.py          # SearchSentinelAgent + 8 MCP tools + SerpApi integration
│   └── store.py          # Lightweight in-memory time-series store (rankings, baselines)
├── static/index.html     # Dark "search intelligence" dashboard UI
├── tests/test_smoke.py   # TestClient smoke tests
├── vercel.json           # Vercel build config
├── requirements.txt
├── CONCEPT.md            # This file
├── README.md
└── LICENSE               # Apache 2.0
```

**Stack:** FastAPI (Python) backend, SerpApi for live data, statistical anomaly detection
(z-score + Jaccard + EWMA), MCP-compatible tool endpoints, Vercel free-tier serverless deploy.

## Demo Mode (no SerpApi key)

Every tool works with realistic mock SERP data so the project is fully demonstrable to judges
out of the box. Setting `SERPAPI_API_KEY` switches all tools to live SerpApi data with no code
changes. This is critical because SerpApi free credits are limited and judges may not have a key.

## Deployment Plan

- **Hosting:** Vercel free tier (same pattern as our prior FastAPI/MCP deployments)
- **Repo:** `github.com/0xConsole/search-sentinel` (public, Apache 2.0)
- **Live URL:** `search-sentinel.vercel.app` (or similar)
- **No paid services required.** Vercel free + SerpApi free credits cover the whole demo.

## Expected Value

$2,000 (cash + credits) × P(0.20–0.35) = **$400–$700 EV**
- Smaller competition pool (only SerpApi-track entrants)
- Novel use case (anomaly detection, not another SEO dashboard)
- Working MCP agent (judges favor agent patterns)
- Two entries in the same track maximizes coverage
