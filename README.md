# SearchSentinel — Real-Time Search Intelligence & Anomaly Detection Agent

> An autonomous AI agent that uses **SerpApi** live search data to monitor the web and detect
> anomalies in search rankings, result composition, and query volume — before they show up
> in any lagging dashboard. Built for the **DevNetwork Hackathon 2026** SerpApi track.

**Live demo:** https://search-sentinel.vercel.app  •  **Repo:** https://github.com/0xConsole/search-sentinel

---

## What it does

Search is the world's largest real-time signal of what people care about. Sudden ranking
shifts, result-set churn, and volume spikes are early indicators of breaking news, viral
events, brand crises, and search algorithm updates. **SearchSentinel watches continuously
and flags anomalies with context** — so a human never has to stare at a dashboard.

Every capability is exposed as an **MCP-compatible tool**, so SearchSentinel can be orchestrated
by any AI agent — it's not just a standalone web app.

### The 8 MCP tools

| # | Tool | What it does |
|---|------|--------------|
| 1 | `serp_monitor` | Pull live SERP for a query (organic, news, answer box, related, PAA) via SerpApi |
| 2 | `track_rankings` | Track a query's top-10 ranking positions; record a time-series snapshot |
| 3 | `detect_ranking_anomalies` | Z-score detection of ranking volatility across snapshots |
| 4 | `detect_result_set_churn` | Jaccard distance vs baseline — flag new/disappeared results |
| 5 | `detect_volume_anomalies` | Anomalies in result-count & related-query volume proxies |
| 6 | `correlate_anomalies` | Cross-query correlation to detect algorithm-update-scale events |
| 7 | `generate_intelligence_report` | Auto-generate a full Markdown + JSON intelligence report |
| 8 | `list_tracking_queries` | Inventory of tracked queries + current anomaly scores |

### How anomaly detection works

SearchSentinel uses proven **statistical** methods (no ML training data needed — works on
day one):

- **Ranking volatility** — z-score of mean rank vs the query's historical snapshots. |z| ≥ 1.5 ⇒ anomaly.
- **Result-set churn** — Jaccard distance between the current top-10 URLs and the baseline snapshot. Churn ≥ 0.35 ⇒ anomaly.
- **Volume spike** — z-score of total result count vs the query's historical mean. |z| ≥ 2.0 ⇒ anomaly.
- **Correlation** — when ≥2 tracked queries show simultaneous anomalies, SearchSentinel flags a probable algorithm-update-scale event.

## Quick start (local)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://localhost:8000
```

### Live SerpApi mode

SearchSentinel works out of the box with realistic mock SERP data (demo mode). To use live
SerpApi data, set one environment variable:

```bash
export SERPAPI_API_KEY="your_serpapi_key"
```

All 8 tools switch to live SerpApi data with no code changes.

## API

### REST endpoints (one per tool — easy to curl)

```
GET /api/health
GET /api/agent/status
GET /api/mcp/tools
GET /api/demo                        # full autonomous monitoring cycle (the judge demo)
GET /api/tools/serp_monitor?query=...
GET /api/tools/track_rankings?query=...
GET /api/tools/detect_ranking_anomalies?query=...
GET /api/tools/detect_result_set_churn?query=...
GET /api/tools/detect_volume_anomalies?query=...
GET /api/tools/correlate_anomalies
GET /api/tools/generate_intelligence_report?query=...
GET /api/tools/list_tracking_queries
```

### MCP protocol endpoint (POST — for agent orchestration)

```bash
curl -X POST https://search-sentinel.vercel.app/api/mcp \
  -H "Content-Type: application/json" \
  -d '{"tool":"detect_ranking_anomalies","args":{"query":"artificial intelligence"}}'
```

## Architecture

```
search-sentinel/
├── api/index.py          # Vercel serverless entry → FastAPI app
├── app/
│   ├── main.py           # FastAPI app, routes, MCP endpoint, demo endpoint
│   ├── agent.py          # SearchSentinelAgent + 8 MCP tools + SerpApi + anomaly detection
│   └── store.py          # In-memory time-series store (snapshots, baselines, anomalies)
├── static/index.html     # Dark "search intelligence" dashboard UI
├── tests/test_smoke.py   # TestClient smoke tests
├── vercel.json
├── requirements.txt
├── CONCEPT.md
└── LICENSE
```

**Stack:** FastAPI (Python) · SerpApi (live data) · statistical anomaly detection
(z-score + Jaccard + EWMA) · MCP-compatible tool endpoints · Vercel free-tier serverless.

## Why this is novel for the SerpApi track

Most SerpApi hackathon entries build SEO dashboards, price trackers, or "chat with search"
demos. **Statistical anomaly detection on live SERPs** is an underexplored, defensible use
case — and exposing it all as MCP tools makes SearchSentinel composable into larger agent
workflows rather than a dead-end web app.

## License

Apache 2.0 — see [LICENSE](LICENSE).

## Hackathon

DevNetwork [API + Cloud + AI] Hackathon 2026 · SerpApi "Best AI Use Case" track
($1,000 + $1,000 SerpApi credits). Built by [0xConsole](https://github.com/0xConsole).
