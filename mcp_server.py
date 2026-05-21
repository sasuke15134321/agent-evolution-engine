#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Evolution Engine - MCP Server
Exposes evolution_analyze as an MCP tool.

Transport (standalone): stdio  →  python mcp_server.py
Transport (HTTP):       mounted at /mcp inside FastAPI via main.py

Base URL : EVOLUTION_API_BASE_URL env var (default: https://agent-evolution-engine.onrender.com)
Payment  : MCP_PAYMENT_TOKEN env var → PAYMENT-SIGNATURE header
"""

import os
import json
from typing import Optional, List, Dict, Any

import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = os.getenv(
    "EVOLUTION_API_BASE_URL", "https://agent-evolution-engine.onrender.com"
).rstrip("/")
PAYMENT_TOKEN = os.getenv("MCP_PAYMENT_TOKEN", "")

mcp = FastMCP("Agent Evolution Engine")


def _headers() -> dict:
    h = {"Content-Type": "application/json"}
    if PAYMENT_TOKEN:
        h["PAYMENT-SIGNATURE"] = PAYMENT_TOKEN
    return h


async def _post(path: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(f"{BASE_URL}{path}", json=payload, headers=_headers())
        if resp.status_code == 402:
            return {"error": "Payment Required (x402)", "x402": resp.json()}
        resp.raise_for_status()
        return resp.json()


# ── Tools ──────────────────────────────────────────────────────────────────────

@mcp.tool()
async def evolution_analyze(
    ecosystem_id: str,
    current_apis: List[str],
    goals: List[str],
    constraints: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Orchestrate security, budget, memory, and audit checks for an AI agent workflow (0.20 USDC).
    Analyzes the current API ecosystem and returns an evolution plan with replacement/addition recommendations.

    Args:
        ecosystem_id:  Unique identifier for the agent ecosystem being analyzed
        current_apis:  List of API URLs currently in use (e.g. ["https://api.example.com/scan"])
        goals:         Evolution goals (e.g. ["improve_security", "reduce_cost", "add_audit_log"])
        constraints:   Optional constraints dict (e.g. {"max_cost_usdc": 1.0, "latency_ms": 500})

    Returns:
        JSON with evolution_plan, apis_to_replace, apis_to_add,
        estimated_improvement, implementation_steps, next_recommended
    """
    result = await _post("/api/evolution/analyze", {
        "ecosystem_id": ecosystem_id,
        "current_apis": current_apis,
        "goals": goals,
        "constraints": constraints or {},
    })
    return json.dumps(result, ensure_ascii=False, indent=2)


# ── Entry point (stdio transport for local / Claude Code usage) ────────────────

if __name__ == "__main__":
    mcp.run()
