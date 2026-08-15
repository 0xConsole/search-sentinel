"""
SearchSentinel — FastAPI Main Application

Real-time search intelligence & anomaly detection agent powered by SerpApi + MCP.
"""
from __future__ import annotations

import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.agent import (
    search_sentinel,
    TOOL_MAP,
    SERPAPI_KEY,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(
    title="SearchSentinel",
    description="AI agent for real-time search intelligence & anomaly detection — powered by SerpApi + MCP",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Routes ----------

@app.get("/")
async def root():
    """Serve the web UI."""
    index = PROJECT_ROOT / "static" / "index.html"
    if index.exists():
        return HTMLResponse(index.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>SearchSentinel</h1><p>UI not found. See <a href='/api/health'>/api/health</a></p>")


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "service": "SearchSentinel",
        "agent": "SearchSentinel Agent",
        "serpapi_mode": "LIVE" if SERPAPI_KEY else "DEMO (mock — set SERPAPI_API_KEY)",
        "version": "1.0.0",
        "tools_count": len(search_sentinel.tools),
        "timestamp": time.time(),
    }


@app.get("/api/agent/status")
async def agent_status():
    """Get agent configuration and tool inventory."""
    return {
        "agent_name": "SearchSentinel",
        "description": "Autonomous search-intelligence agent — real-time SERP monitoring + anomaly detection via SerpApi",
        "platform": "SerpApi + MCP-compatible tools",
        "model": "Statistical anomaly detection engine (z-score, Jaccard, EWMA)",
        "tools": search_sentinel.tools,
        "mcp_compatible": True,
        "serpapi_enabled": bool(SERPAPI_KEY),
    }


# ---------- MCP tool endpoints (GET for easy browser/curl testing) ----------

@app.get("/api/tools/serp_monitor")
async def tool_serp_monitor(query: str = "artificial intelligence", engine: str = "google"):
    return search_sentinel.serp_monitor(query, engine=engine)


@app.get("/api/tools/track_rankings")
async def tool_track_rankings(query: str = "artificial intelligence", engine: str = "google"):
    return search_sentinel.track_rankings(query, engine=engine)


@app.get("/api/tools/detect_ranking_anomalies")
async def tool_detect_ranking_anomalies(query: str = "artificial intelligence"):
    return search_sentinel.detect_ranking_anomalies(query)


@app.get("/api/tools/detect_result_set_churn")
async def tool_detect_result_set_churn(query: str = "artificial intelligence"):
    return search_sentinel.detect_result_set_churn(query)


@app.get("/api/tools/detect_volume_anomalies")
async def tool_detect_volume_anomalies(query: str = "artificial intelligence"):
    return search_sentinel.detect_volume_anomalies(query)


@app.get("/api/tools/correlate_anomalies")
async def tool_correlate_anomalies():
    return search_sentinel.correlate_anomalies()


@app.get("/api/tools/generate_intelligence_report")
async def tool_generate_intelligence_report(query: str = "artificial intelligence"):
    return search_sentinel.generate_intelligence_report(query)


@app.get("/api/tools/list_tracking_queries")
async def tool_list_tracking_queries():
    return search_sentinel.list_tracking_queries()


# ---------- MCP tools listing (for agent discovery) ----------

@app.get("/api/mcp/tools")
async def mcp_tools():
    """List all MCP-compatible tools for agent orchestration."""
    return {
        "protocol": "MCP-compatible",
        "server": "SearchSentinel",
        "tools": search_sentinel.tools,
        "count": len(search_sentinel.tools),
        "endpoints": {
            "serp_monitor": "/api/tools/serp_monitor?query=<q>&engine=google",
            "track_rankings": "/api/tools/track_rankings?query=<q>",
            "detect_ranking_anomalies": "/api/tools/detect_ranking_anomalies?query=<q>",
            "detect_result_set_churn": "/api/tools/detect_result_set_churn?query=<q>",
            "detect_volume_anomalies": "/api/tools/detect_volume_anomalies?query=<q>",
            "correlate_anomalies": "/api/tools/correlate_anomalies",
            "generate_intelligence_report": "/api/tools/generate_intelligence_report?query=<q>",
            "list_tracking_queries": "/api/tools/list_tracking_queries",
        },
    }


# ---------- MCP protocol endpoint (POST — for agent orchestration) ----------

@app.post("/api/mcp")
async def mcp_endpoint(request: dict):
    """
    Model Context Protocol compatible endpoint.
    Accepts: {"tool": "<name>", "args": {...}}  and dispatches to the agent tool.
    """
    tool_name = request.get("tool")
    args = request.get("args", {})
    if tool_name not in TOOL_MAP:
        return JSONResponse(
            {"error": f"Unknown tool: {tool_name}", "available": list(TOOL_MAP.keys())},
            status_code=404,
        )
    try:
        result = TOOL_MAP[tool_name](**args)
        return {"tool": tool_name, "result": result}
    except Exception as e:
        return JSONResponse({"error": str(e), "tool": tool_name}, status_code=500)


# ---------- Demo endpoint ----------

@app.get("/api/demo")
async def demo():
    """
    Run a full autonomous monitoring cycle — the demo flow for judges.
    """
    return search_sentinel.run_monitoring_cycle("artificial intelligence")
