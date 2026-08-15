"""
SearchSentinel — smoke tests via FastAPI TestClient.
Run: python -m pytest tests/test_smoke.py -v  (or: python tests/test_smoke.py)
"""
import sys
import os
import json

# ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)
PASSED = []


def check(name, cond):
    PASSED.append((name, bool(cond)))
    if not cond:
        raise AssertionError(name)


def main():
    # 1. root serves the dashboard
    r = c.get("/")
    check("GET / 200 + SearchSentinel title", r.status_code == 200 and "SearchSentinel" in r.text)

    # 2. health
    h = c.get("/api/health").json()
    check("GET /api/health ok + 8 tools",
          h["status"] == "ok" and h["tools_count"] == 8 and h["service"] == "SearchSentinel")

    # 3. MCP tools list — must have >=6 (we have 8)
    tl = c.get("/api/mcp/tools").json()
    check("GET /api/mcp/tools count>=6", tl["count"] >= 6 and len(tl["tools"]) >= 6)
    tool_names = {t["name"] for t in tl["tools"]}
    required = {"serp_monitor", "detect_ranking_anomalies", "generate_intelligence_report"}
    check("required tools present", required.issubset(tool_names))

    # 4. agent status
    a = c.get("/api/agent/status").json()
    check("GET /api/agent/status 8 tools + mcp", a["mcp_compatible"] is True and len(a["tools"]) == 8)

    # 5. serp_monitor returns organic results
    sm = c.get("/api/tools/serp_monitor", params={"query": "test query"}).json()
    check("serp_monitor returns organic", isinstance(sm.get("organic"), list) and len(sm["organic"]) > 0)

    # 6. track_rankings records a snapshot
    tr = c.get("/api/tools/track_rankings", params={"query": "openai gpt"}).json()
    check("track_rankings records snapshot", tr["snapshot"]["snapshot_count"] >= 1 and len(tr["current_top10"]) > 0)

    # 7. detect_ranking_anomalies (build history first)
    for _ in range(3):
        c.get("/api/tools/track_rankings", params={"query": "anomaly test query"})
    ra = c.get("/api/tools/detect_ranking_anomalies", params={"query": "anomaly test query"}).json()
    check("detect_ranking_anomalies returns z_score", "z_score" in ra and "is_anomaly" in ra)

    # 8. detect_result_set_churn
    c.get("/api/tools/track_rankings", params={"query": "churn test"})
    c.get("/api/tools/track_rankings", params={"query": "churn test"})
    rc = c.get("/api/tools/detect_result_set_churn", params={"query": "churn test"}).json()
    check("detect_result_set_churn returns churn_score", "churn_score" in rc and "is_anomaly" in rc)

    # 9. detect_volume_anomalies
    va = c.get("/api/tools/detect_volume_anomalies", params={"query": "volume test"}).json()
    check("detect_volume_anomalies returns total_results", "total_results" in va and "is_anomaly" in va)

    # 10. correlate_anomalies
    co = c.get("/api/tools/correlate_anomalies").json()
    check("correlate_anomalies returns correlated flag", "correlated" in co and "per_query" in co)

    # 11. generate_intelligence_report
    rep = c.get("/api/tools/generate_intelligence_report", params={"query": "report test"}).json()
    check("report has id+markdown+status",
          "report_id" in rep and "markdown" in rep and "overall_status" in rep)
    check("report markdown contains title", "SearchSentinel Intelligence Report" in rep["markdown"])

    # 12. list_tracking_queries
    lt = c.get("/api/tools/list_tracking_queries").json()
    check("list_tracking_queries returns queries_tracked",
          "queries_tracked" in lt and lt["queries_tracked"] >= 1)

    # 13. MCP POST endpoint dispatch
    mp = c.post("/api/mcp", json={"tool": "serp_monitor", "args": {"query": "mcp test"}}).json()
    check("MCP POST dispatches serp_monitor", mp["tool"] == "serp_monitor" and "organic" in mp["result"])

    # 14. MCP POST unknown tool -> 404 with available list
    err = c.post("/api/mcp", json={"tool": "does_not_exist", "args": {}}).json()
    check("MCP POST unknown tool 404 + available", "error" in err and "available" in err)

    # 15. demo endpoint — full monitoring cycle
    d = c.get("/api/demo").json()
    check("GET /api/demo complete + 6 steps",
          d["demo_complete"] is True and d["total_steps"] == 6 and "report_id" in d)

    # 16. vercel.json + requirements.txt valid
    with open(os.path.join(os.path.dirname(__file__), "..", "vercel.json")) as f:
        vj = json.load(f)
    check("vercel.json valid", "builds" in vj and "routes" in vj)

    # summary
    npass = sum(1 for _, ok in PASSED if ok)
    print(f"\nSmoke tests: {npass}/{len(PASSED)} PASSED")
    for name, ok in PASSED:
        print(f"  {'PASS' if ok else 'FAIL'}: {name}")
    if npass != len(PASSED):
        sys.exit(1)


if __name__ == "__main__":
    main()
