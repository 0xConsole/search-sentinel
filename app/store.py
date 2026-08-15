"""
SearchSentinel — In-memory time-series store for rankings, baselines, and anomaly history.

Vercel serverless functions are stateless across cold starts, but within a warm instance
the store persists across requests, which is enough for the demo + MCP orchestration
use case. For production this would be swapped for Redis/Postgres behind the same interface.
"""
from __future__ import annotations

import time
from collections import defaultdict
from typing import Any


class SentinelStore:
    """Lightweight in-memory store: per-query ranking snapshots, baselines, anomalies."""

    def __init__(self) -> None:
        # query -> list of {"timestamp", "rankings": [ {position, title, url, domain} ]}
        self.history: dict[str, list[dict[str, Any]]] = defaultdict(list)
        # query -> set of baseline result URLs (first snapshot becomes the baseline)
        self.baselines: dict[str, set[str]] = {}
        # query -> list of detected anomalies
        self.anomalies: dict[str, list[dict[str, Any]]] = defaultdict(list)
        # query -> EWMA of mean rank (for volatility tracking)
        self.ewma_mean_rank: dict[str, float] = {}
        # query -> first-seen timestamp (for "tracking since")
        self.tracking_since: dict[str, float] = {}

    # ----- snapshots -----

    def add_snapshot(self, query: str, rankings: list[dict[str, Any]]) -> dict[str, Any]:
        """Record a SERP snapshot for a query. rankings = list of {position,title,url,domain}."""
        ts = time.time()
        if query not in self.tracking_since:
            self.tracking_since[query] = ts
            self.baselines[query] = {r.get("url", "") for r in rankings}

        self.history[query].append({"timestamp": ts, "rankings": rankings})

        # keep only the last 50 snapshots per query to bound memory
        if len(self.history[query]) > 50:
            self.history[query] = self.history[query][-50:]

        # update EWMA of mean rank (alpha = 0.3)
        positions = [r.get("position", 0) for r in rankings]
        mean_rank = sum(positions) / len(positions) if positions else 0.0
        if query in self.ewma_mean_rank:
            self.ewma_mean_rank[query] = 0.7 * self.ewma_mean_rank[query] + 0.3 * mean_rank
        else:
            self.ewma_mean_rank[query] = mean_rank

        return {
            "query": query,
            "snapshot_count": len(self.history[query]),
            "tracking_since": self.tracking_since[query],
            "mean_rank_ewma": round(self.ewma_mean_rank[query], 3),
        }

    def get_snapshots(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        return self.history.get(query, [])[-limit:]

    # ----- anomalies -----

    def record_anomaly(self, query: str, anomaly: dict[str, Any]) -> None:
        anomaly["recorded_at"] = time.time()
        self.anomalies[query].append(anomaly)
        if len(self.anomalies[query]) > 100:
            self.anomalies[query] = self.anomalies[query][-100:]

    def get_anomalies(self, query: str, limit: int = 20) -> list[dict[str, Any]]:
        return self.anomalies.get(query, [])[-limit:]

    # ----- queries -----

    def list_queries(self) -> list[str]:
        return sorted(self.history.keys())

    def query_summary(self, query: str) -> dict[str, Any]:
        snaps = self.history.get(query, [])
        anomalies = self.anomalies.get(query, [])
        return {
            "query": query,
            "snapshots": len(snaps),
            "anomalies": len(anomalies),
            "tracking_since": self.tracking_since.get(query),
            "mean_rank_ewma": round(self.ewma_mean_rank.get(query, 0.0), 3),
            "baseline_urls": len(self.baselines.get(query, set())),
        }


# module-level singleton — persists across requests within a warm instance
store = SentinelStore()
