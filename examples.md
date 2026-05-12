# Agent Evolution Engine API - Examples

## Example 1: エコシステム全体の分析と進化計画生成
### Request
```bash
curl -X POST https://agent-evolution-engine.onrender.com/api/evolution/analyze \
  -H "Content-Type: application/json" \
  -H "X-PAYMENT: <x402_token>" \
  -d '{
    "agent_id": "agent-001",
    "current_apis": ["agent-memory-api", "agent-security-gateway"],
    "goals": ["cost_reduction", "japanese_optimization", "reliability"],
    "budget_usdc_daily": 5.00,
    "analysis_depth": "comprehensive"
  }'
```
### Response
```json
{
  "evolution_plan": {
    "current_score": 65,
    "projected_score": 88,
    "recommended_additions": [
      {
        "api": "Agent Budget Guard",
        "reason": "No spending controls detected",
        "expected_savings_usdc": 1.20,
        "priority": "high"
      },
      {
        "api": "Agent Curator API",
        "reason": "Can optimize API selection automatically",
        "priority": "medium"
      }
    ],
    "optimization_steps": [
      "Add budget guard before every x402 payment",
      "Enable memory compression to reduce recall costs",
      "Use curator API for dynamic API switching"
    ]
  },
  "estimated_monthly_cost_usdc": 45.00,
  "next_evolution_check": "2026-06-13"
}
```

## Example 2: 定期的な進化状態のチェック
### Request
```bash
curl -X GET https://agent-evolution-engine.onrender.com/api/evolution/status/agent-001 \
  -H "X-PAYMENT: <x402_token>"
```
### Response
```json
{
  "agent_id": "agent-001",
  "evolution_stage": 3,
  "apis_integrated": 4,
  "efficiency_score": 78,
  "last_evolution": "2026-05-01T00:00:00Z",
  "next_recommended_evolution": "2026-06-01T00:00:00Z",
  "active_optimizations": [
    "Budget guard enabled for all payments",
    "Memory TTL optimized to 12h (was 24h)"
  ]
}
```

## Example 3: 自律進化の実行
### Request
```bash
curl -X POST https://agent-evolution-engine.onrender.com/api/evolution/evolve \
  -H "Content-Type: application/json" \
  -H "X-PAYMENT: <x402_token>" \
  -d '{
    "agent_id": "agent-001",
    "auto_apply": false,
    "evolution_target": "cost_efficiency"
  }'
```
### Response
```json
{
  "proposed_changes": [
    {
      "change": "Reduce memory TTL from 86400s to 43200s",
      "impact": "Save 0.30 USDC/day",
      "risk": "low"
    },
    {
      "change": "Add security scan before all external API calls",
      "impact": "Increase safety score by 15 points",
      "cost": "0.05 USDC/call"
    }
  ],
  "estimated_improvement": "+18% efficiency",
  "apply_url": "POST /api/evolution/apply/agent-001"
}
```
