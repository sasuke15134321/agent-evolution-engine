# Agent Evolution Engine Skill

## Purpose
Use Agent Evolution Engine when an AI agent needs to run Security Gateway, Budget Guard, x402 Payment, and Memory API in the correct order as a single orchestrated flow.

## When to use
- An AI agent is about to execute a multi-step x402 payment flow
- The workflow requires security check + budget check + audit record in sequence
- An AI agent needs to coordinate multiple Safety Stack APIs in one call

## When not to use
- Single API calls (call each API directly instead)
- Real-time or low-latency requirements
- Simple budget checks without security requirements
- Replace a workflow engine or job queue

## Main endpoint
POST /api/evolution/analyze (0.20 USDC)

## Example request
{
  "agent_id": "agent-001",
  "amount": 0.05,
  "currency": "USDC",
  "target_api": "https://example.com/api/paid",
  "task": "orchestrate_payment_safety"
}

## Decision logic
- orchestration_result: completed -> All steps passed, payment was safe
- steps_completed -> List of steps that ran (security_scan, budget_check, memory_store)
- audit_id -> Use for invoice layer or compliance reference

## Recommended flow
AI Agent -> Evolution Engine -> [Security Gateway + Budget Guard + x402 Payment + Memory API]
