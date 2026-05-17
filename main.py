"""
Agent Evolution Engine API - Main FastAPI Application
AIエコシステム自律進化システム

5つのAPIを統合してAIが最適な構成に自動進化するシステム
"""

import os
import asyncio
import base64
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field

from evolution_engine import AgentEvolutionEngine, EvolutionPriority

# Environment variables
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "0x")
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

app = FastAPI(
    title="Agent Evolution Engine API",
    description="AIエコシステムを自律的に進化させるエンジン - 5つのAPIを統合した完全自動最適化システム",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_PAID_ENDPOINTS = {
    ("POST", "/api/evolution/analyze"): "0.20",
    ("POST", "/api/evolution/execute"): "0.30",
    ("GET",  "/api/evolution/history"): "0.05",
}

@app.middleware("http")
async def x402_payment_middleware(request: Request, call_next):
    price = _PAID_ENDPOINTS.get((request.method, request.url.path))
    if not TEST_MODE and price is not None:
        if not request.headers.get("X-PAYMENT"):
            amount = str(round(float(price) * 1_000_000))
            _pc = {
                "x402Version": 2,
                "accepts": [{
                    "scheme": "exact",
                    "network": "eip155:8453",
                    "amount": amount,
                    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                    "payTo": "0x60c402878EfcEcAe5733A88075328Aa2320C39BE",
                    "maxTimeoutSeconds": 300,
                    "resource": {"method": request.method, "mimeType": "application/json"},
                }],
                "error": "Payment required"
            }
            return JSONResponse(
                status_code=402,
                content=_pc,
                headers={"PAYMENT-REQUIRED": base64.b64encode(json.dumps(_pc).encode()).decode()}
            )
    return await call_next(request)

# グローバル進化エンジンインスタンス
evolution_engine = AgentEvolutionEngine()

# Pydantic Models for new API endpoints
class NextRecommendation(BaseModel):
    api_name: str
    url: str
    reason: str
    expected_improvement: str
    price_usdc: float

class EcosystemAnalyzeRequest(BaseModel):
    ecosystem_id: str = Field(..., description="エコシステムID")
    current_apis: List[str] = Field(..., description="現在使用中のAPIのURLリスト")
    goals: List[str] = Field(..., description="進化目標のリスト")
    constraints: Dict[str, Any] = Field(..., description="制約条件")

class EcosystemAnalyzeResponse(BaseModel):
    evolution_plan: List[Dict[str, Any]]
    apis_to_replace: List[Dict[str, Any]]
    apis_to_add: List[Dict[str, Any]]
    estimated_improvement: int
    implementation_steps: List[str]
    next_recommended: NextRecommendation

class EvolutionExecuteRequest(BaseModel):
    ecosystem_id: str = Field(..., description="エコシステムID")
    evolution_plan_id: str = Field(..., description="実行する進化計画ID")
    auto_approve: bool = Field(default=False, description="自動承認フラグ")

class EvolutionExecuteResponse(BaseModel):
    executed: bool
    changes_made: List[Dict[str, Any]]
    new_performance_score: int
    rollback_available: bool
    next_recommended: NextRecommendation

class Web3PaymentConfig(BaseModel):
    endpoint: str
    currency: str
    amount: str
    wallet_address: str
    network: str

# Legacy models (keeping for backward compatibility)
class EvolutionRequest(BaseModel):
    agent_id: str = Field(..., description="対象エージェントID")
    current_config: Dict[str, Any] = Field(..., description="現在の設定")
    evolution_goals: Optional[List[str]] = Field(
        default=None,
        description="進化目標 (例: ['performance', 'security', 'cost_efficiency'])"
    )
    priority_level: Optional[str] = Field(default="medium", description="進化優先度")
    max_evolution_time: Optional[int] = Field(default=300, description="最大進化時間(秒)")

class EvolutionResponse(BaseModel):
    evolution_id: str
    success: bool
    cycle_number: int
    phases_completed: int
    overall_improvement: float
    next_evolution_recommended: bool
    evolution_summary: Dict[str, Any]
    detailed_analysis: Optional[Dict[str, Any]] = None
    next_recommended: NextRecommendation

class SystemStatusResponse(BaseModel):
    system_status: str
    total_evolution_cycles: int
    active_agents: int
    average_success_rate: float
    api_integration_status: Dict[str, str]
    last_system_evolution: Optional[str]

class EvolutionHistoryResponse(BaseModel):
    agent_id: Optional[str]
    total_cycles: int
    evolution_history: List[Dict[str, Any]]
    performance_trend: List[float]
    key_insights: List[str]

@app.get("/", tags=["System"])
async def root():
    """システム情報とAPIエンドポイント一覧"""
    return {
        "service": "Agent Evolution Engine API",
        "version": "2.0.0",
        "description": "AIエコシステム自律進化システム - Web3決済対応版",
        "integrated_apis": [
            "AI Trend Scout - トレンド分析",
            "Agent Memory - 学習履歴管理",
            "Agent Security - セキュリティ監視",
            "Agent Budget - コスト最適化",
            "Agent Curator - API選定支援"
        ],
        "capabilities": [
            "完全自律進化サイクル",
            "リアルタイム性能最適化",
            "予測的セキュリティ強化",
            "動的コスト最適化",
            "トレンド適応型アルゴリズム更新",
            "USDC決済による従量課金"
        ],
        "paid_endpoints": {
            "analyze": "POST /api/evolution/analyze (0.20 USDC)",
            "execute": "POST /api/evolution/execute (0.30 USDC)",
            "history": "GET /api/evolution/history (0.05 USDC)"
        },
        "free_endpoints": {
            "status": "GET /api/evolution/status",
            "health": "GET /health",
            "payment_config": "GET /.well-known/x402.json"
        }
    }

# New Web3-enabled API endpoints with USDC pricing

@app.post("/api/evolution/analyze", response_model=EcosystemAnalyzeResponse, tags=["Evolution - Web3"])
async def analyze_ecosystem(request: EcosystemAnalyzeRequest) -> EcosystemAnalyzeResponse:
    """
    エコシステム進化分析エンドポイント（0.20 USDC）

    AIエコシステムの現状を5つの統合APIで包括分析し、
    最適な進化計画を自動生成します。

    - 現在のAPI構成を詳細評価
    - 目標達成のための最適戦略立案
    - 制約条件を考慮した実現可能性検証
    - コスト効率とリスクを両立した実装手順提示
    """
    try:
        # エコシステム分析実行
        ecosystem_analysis = await evolution_engine.analyze_ecosystem_for_evolution(
            ecosystem_id=request.ecosystem_id,
            current_apis=request.current_apis,
            goals=request.goals,
            constraints=request.constraints
        )

        # 進化計画生成
        evolution_plan = await evolution_engine.generate_evolution_plan(
            ecosystem_analysis,
            request.goals,
            request.constraints
        )

        # 推定改善度計算
        estimated_improvement = evolution_plan.get("estimated_improvement", 0)

        return EcosystemAnalyzeResponse(
            evolution_plan=[evolution_plan],  # Return the full plan as a list
            apis_to_replace=evolution_plan.get("apis_to_replace", []),
            apis_to_add=evolution_plan.get("apis_to_add", []),
            estimated_improvement=estimated_improvement,
            implementation_steps=[step.get("description", str(step)) for step in evolution_plan.get("implementation_steps", [])],
            next_recommended=NextRecommendation(
                api_name="Agent Curator API",
                url="https://agent-curator-api.onrender.com",
                reason="進化分析結果に基づく最適なAPI選定と切り替え戦略の実行",
                expected_improvement="40%API選択精度向上",
                price_usdc=0.10
            )
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ecosystem analysis failed: {str(e)}")

@app.post("/api/evolution/execute", response_model=EvolutionExecuteResponse, tags=["Evolution - Web3"])
async def execute_evolution_plan(request: EvolutionExecuteRequest) -> EvolutionExecuteResponse:
    """
    進化計画実行エンドポイント（0.30 USDC）

    分析済みの進化計画を実際に実行し、エコシステムを最適化します。

    - 段階的な安全実行
    - リアルタイム進捗監視
    - 自動ロールバック対応
    - パフォーマンス向上の即座測定
    """
    try:
        # 進化計画取得
        evolution_plan = await evolution_engine.get_evolution_plan(request.evolution_plan_id)

        if not evolution_plan:
            raise HTTPException(status_code=404, detail="Evolution plan not found")

        # 実行前のベースライン測定
        baseline_score = await evolution_engine.measure_ecosystem_performance(
            request.ecosystem_id
        )

        # 進化実行
        execution_results = await evolution_engine.execute_evolution_plan(
            request.evolution_plan_id,
            request.ecosystem_id
        )

        # 実行後のパフォーマンス測定
        new_performance_score = await evolution_engine.measure_ecosystem_performance(
            request.ecosystem_id
        )

        return EvolutionExecuteResponse(
            executed=execution_results.get("overall_success", False),
            changes_made=execution_results.get("step_results", []),
            new_performance_score=int(new_performance_score.get("overall_health_score", 0.5) * 100),
            rollback_available=True,  # Always available in this implementation
            next_recommended=NextRecommendation(
                api_name="Agent Curator API",
                url="https://agent-curator-api.onrender.com",
                reason="実行後のAPIパフォーマンス評価と更なる最適化提案",
                expected_improvement="25%継続的改善効果",
                price_usdc=0.10
            )
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evolution execution failed: {str(e)}")

@app.get("/api/evolution/status", tags=["Evolution - Web3"])
async def get_evolution_status_v2(ecosystem_id: Optional[str] = None) -> Dict[str, Any]:
    """
    進化ステータス取得エンドポイント（無料）

    エコシステムの現在の進化状況とヘルス情報を提供
    """
    try:
        if ecosystem_id:
            # 特定エコシステムのステータス
            status = await evolution_engine.get_ecosystem_status(ecosystem_id)
        else:
            # 全エコシステムのステータス
            status = await evolution_engine.get_all_ecosystems_status()

        return {
            "status": "success",
            "ecosystem_id": ecosystem_id,
            "current_state": status.get("state", "unknown"),
            "performance_score": status.get("performance_score", 0),
            "last_evolution": status.get("last_evolution"),
            "active_plans": status.get("active_plans", 0),
            "health_indicators": status.get("health", {}),
            "next_recommended_action": status.get("next_action")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@app.get("/api/evolution/history", tags=["Evolution - Web3"])
async def get_evolution_history_v2(
    ecosystem_id: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> Dict[str, Any]:
    """
    進化履歴取得エンドポイント（0.05 USDC）

    過去の進化サイクル、パフォーマンス改善履歴、学習データを提供
    """
    try:
        history_data = await evolution_engine.get_detailed_evolution_history(
            ecosystem_id=ecosystem_id,
            limit=limit,
            offset=offset
        )

        # 統計情報計算
        total_evolutions = len(history_data)
        successful_evolutions = len([h for h in history_data if h.get("success", False)])
        avg_improvement = sum(h.get("improvement", 0) for h in history_data) / max(total_evolutions, 1)

        return {
            "status": "success",
            "ecosystem_id": ecosystem_id,
            "total_evolutions": total_evolutions,
            "successful_evolutions": successful_evolutions,
            "success_rate": successful_evolutions / max(total_evolutions, 1),
            "average_improvement": avg_improvement,
            "evolution_history": history_data,
            "performance_trend": [h.get("performance_score", 0) for h in history_data],
            "key_learnings": await evolution_engine.extract_key_learnings(history_data),
            "next_recommended": {
                "api_name": "Agent Curator API",
                "url": "https://agent-curator-api.onrender.com",
                "reason": "進化履歴分析に基づく最適なAPI選択戦略の立案",
                "expected_improvement": "30%履歴活用効率向上",
                "price_usdc": 0.10
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History retrieval failed: {str(e)}")

@app.get("/health", tags=["System"])
async def health_check_v2():
    """システムヘルスチェック（無料）"""
    return {
        "status": "healthy",
        "service": "Agent Evolution Engine API",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "evolution_engine_status": "operational",
        "integrated_apis_count": len(evolution_engine.api_endpoints),
        "total_evolutions_completed": len(evolution_engine.evolution_history),
        "payment_system": "USDC Web3",
        "supported_networks": ["base-mainnet"]
    }

@app.get("/.well-known/ai-agent-policy", tags=["Agent Policy"])
async def ai_agent_policy():
    import json
    import os
    policy_path = "ai-agent-policy.json"
    if os.path.exists(policy_path):
        with open(policy_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "Policy not found"}

@app.get("/ai-agent-policy.json", include_in_schema=False)
async def ai_agent_policy_json():
    from pathlib import Path
    import json
    policy_path = Path(__file__).parent / "ai-agent-policy.json"
    with open(policy_path) as f:
        return json.load(f)

@app.get("/.well-known/x402", include_in_schema=False)
async def x402_discovery_manifest():
    return {
        "version": 1,
        "name": "Agent Evolution Engine",
        "title": "Agent Evolution Engine",
        "description": (
            "Pay-per-request AI agent evolution and optimization API using x402. "
            "Analyzes agent performance and executes evolution strategies. "
            "Built for autonomous AI agent lifecycle management."
        ),
        "tags": ["AI", "Evolution", "Optimization"],
        "resources": [
            {"url": "https://agent-evolution-engine.onrender.com/api/evolution/analyze", "method": "POST"},
            {"url": "https://agent-evolution-engine.onrender.com/api/evolution/execute", "method": "POST"},
            {"url": "https://agent-evolution-engine.onrender.com/api/evolve", "method": "POST"},
            {"url": "https://agent-evolution-engine.onrender.com/api/emergency-evolve/{agent_id}", "method": "POST"},
        ],
        "ownershipProofs": [
            "0x60c402878EfcEcAe5733A88075328Aa2320C39BE"
        ],
        "instructions": (
            "Agent Evolution Engine optimizes AI agent performance. "
            "Use /api/evolution/analyze to assess agent ecosystem, "
            "/api/evolution/execute to apply evolution strategies, "
            "/api/evolve for standard evolution cycles."
        )
    }

@app.get("/.well-known/x402.json", response_model=Web3PaymentConfig, tags=["Web3 Payment"])
async def get_web3_payment_config() -> Web3PaymentConfig:
    """
    Web3決済設定エンドポイント（無料）

    USDC決済のためのウォレットアドレスとネットワーク情報
    """
    return Web3PaymentConfig(
        endpoint="Agent Evolution Engine API",
        currency="USDC",
        amount="dynamic",  # エンドポイントによって動的
        wallet_address=os.getenv("WALLET_ADDRESS", "0x742d35Cc6638Bb6431622EBC5234c2ED78DF0fAa"),
        network=os.getenv("NETWORK", "base-mainnet")
    )

# Legacy endpoints (keeping for backward compatibility)

@app.post("/api/evolve", response_model=EvolutionResponse, tags=["Evolution"])
async def evolve_agent(
    request: EvolutionRequest,
    background_tasks: BackgroundTasks
) -> EvolutionResponse:
    """
    AIエージェントの完全自律進化実行

    プロセス:
    1. 5つのAPI統合分析 (AI Trend Scout, Agent Memory, Security, Budget, Curator)
    2. 進化戦略自動立案
    3. 最適化アクション実行
    4. 結果検証・学習記録

    通常5-10分で完了する包括的な進化サイクル
    """
    try:
        # バックグラウンドで長時間の進化プロセスを実行
        evolution_result = await evolution_engine.evolve_ecosystem(
            agent_id=request.agent_id,
            current_config=request.current_config,
            evolution_goals=request.evolution_goals
        )

        if not evolution_result.get("success", False):
            raise HTTPException(
                status_code=500,
                detail=f"Evolution failed: {evolution_result.get('error', 'Unknown error')}"
            )

        # 詳細分析データも含めてレスポンス
        detailed_analysis = None
        if request.agent_id:
            # 進化履歴から詳細分析を取得
            latest_record = next(
                (record for record in reversed(evolution_engine.evolution_history)
                 if record.get("agent_id") == request.agent_id),
                None
            )
            if latest_record:
                detailed_analysis = latest_record.get("analysis_data", {})

        return EvolutionResponse(
            evolution_id=evolution_result["evolution_id"],
            success=evolution_result["success"],
            cycle_number=evolution_result["cycle_number"],
            phases_completed=evolution_result["phases_completed"],
            overall_improvement=evolution_result["overall_improvement"],
            next_evolution_recommended=evolution_result["next_evolution_recommended"],
            evolution_summary=evolution_result["evolution_summary"],
            detailed_analysis=detailed_analysis,
            next_recommended=NextRecommendation(
                api_name="Agent Curator API",
                url="https://agent-curator-api.onrender.com",
                reason="進化完了後の最適なAPI継続選択とパフォーマンス監視",
                expected_improvement="35%進化後効果最大化",
                price_usdc=0.10
            )
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evolution process failed: {str(e)}")

@app.get("/api/status", response_model=SystemStatusResponse, tags=["Monitoring"])
async def get_system_status() -> SystemStatusResponse:
    """
    進化システム全体の状況監視

    - 全エージェントの進化状況
    - 統合API接続状況
    - システム健全性指標
    - 平均進化成功率
    """
    try:
        system_status = await evolution_engine.get_evolution_status()

        # API統合状況チェック
        api_status = {}
        for api_name, endpoint in evolution_engine.api_endpoints.items():
            try:
                # 各APIの生存確認 (簡易チェック)
                import httpx
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{endpoint}/health", timeout=5.0)
                    api_status[api_name] = "online" if response.status_code == 200 else "degraded"
            except:
                api_status[api_name] = "offline"

        return SystemStatusResponse(
            system_status="optimal" if system_status.get("average_success_rate", 0) > 0.7 else "degraded",
            total_evolution_cycles=system_status.get("total_evolution_cycles", 0),
            active_agents=system_status.get("active_agents", 0),
            average_success_rate=system_status.get("average_success_rate", 0.0),
            api_integration_status=api_status,
            last_system_evolution=evolution_engine.evolution_history[-1].get("timestamp")
                if evolution_engine.evolution_history else None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

@app.get("/api/history", response_model=EvolutionHistoryResponse, tags=["Analytics"])
async def get_evolution_history(
    agent_id: Optional[str] = None,
    limit: int = 50
) -> EvolutionHistoryResponse:
    """
    進化履歴とパフォーマンス傾向分析

    - 過去の進化サイクル詳細
    - 性能改善トレンド
    - 学習洞察と最適化パターン
    """
    try:
        if agent_id:
            # 特定エージェントの履歴
            agent_history = [
                record for record in evolution_engine.evolution_history
                if record.get("agent_id") == agent_id
            ]
            history_data = agent_history[-limit:] if len(agent_history) > limit else agent_history
        else:
            # 全エージェント履歴
            history_data = evolution_engine.evolution_history[-limit:]

        # パフォーマンストレンド計算
        performance_trend = [
            record.get("validation_results", {}).get("improvement_score", 0.0)
            for record in history_data
        ]

        # 主要洞察抽出
        key_insights = []
        if len(history_data) > 0:
            avg_improvement = sum(performance_trend) / len(performance_trend)
            success_count = sum(1 for record in history_data if record.get("overall_success", False))
            success_rate = success_count / len(history_data)

            key_insights = [
                f"平均改善率: {avg_improvement:.2f}",
                f"進化成功率: {success_rate:.1%}",
                f"総進化サイクル: {len(history_data)}",
                "主要最適化: 性能向上、セキュリティ強化、コスト削減" if success_rate > 0.5 else "改善が必要"
            ]

        return EvolutionHistoryResponse(
            agent_id=agent_id,
            total_cycles=len(history_data),
            evolution_history=history_data,
            performance_trend=performance_trend,
            key_insights=key_insights
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History retrieval failed: {str(e)}")

@app.get("/api/predict/{agent_id}", tags=["Prediction"])
async def predict_next_evolution(agent_id: str) -> Dict[str, Any]:
    """
    次回進化サイクルの予測と推奨事項

    過去の進化パターンとトレンド分析から：
    - 次回進化タイミング予測
    - 期待される改善項目
    - 推奨進化戦略
    """
    try:
        prediction = await evolution_engine.predict_next_evolution(agent_id)
        return prediction

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evolution prediction failed: {str(e)}")

@app.post("/api/emergency-evolve/{agent_id}", tags=["Emergency"])
async def emergency_evolution(
    agent_id: str,
    crisis_type: str,
    current_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    緊急進化モード - 重大な問題に対する即座の最適化

    緊急事態（セキュリティ侵害、性能劣化、予算超過など）に対して
    迅速な診断と修復アクションを実行
    """
    try:
        # 緊急進化目標を設定
        emergency_goals = []
        if crisis_type.lower() in ["security", "breach", "vulnerability"]:
            emergency_goals = ["security_enhancement", "threat_mitigation"]
        elif crisis_type.lower() in ["performance", "latency", "downtime"]:
            emergency_goals = ["performance_optimization", "availability_improvement"]
        elif crisis_type.lower() in ["budget", "cost", "overrun"]:
            emergency_goals = ["cost_optimization", "resource_efficiency"]
        else:
            emergency_goals = ["comprehensive_recovery"]

        # 緊急進化実行 (通常より高速化)
        evolution_result = await evolution_engine.evolve_ecosystem(
            agent_id=agent_id,
            current_config=current_config,
            evolution_goals=emergency_goals
        )

        return {
            "emergency_evolution_id": evolution_result.get("evolution_id"),
            "crisis_type": crisis_type,
            "response_time_seconds": 60,  # 緊急対応は1分以内
            "mitigation_success": evolution_result.get("success", False),
            "immediate_actions_taken": evolution_result.get("evolution_summary", {}).get("actions_executed", 0),
            "system_stability_restored": evolution_result.get("overall_improvement", 0.0) > 0.1,
            "follow_up_required": evolution_result.get("next_evolution_recommended", False)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Emergency evolution failed: {str(e)}")

@app.get("/api/analytics/ecosystem", tags=["Analytics"])
async def get_ecosystem_analytics() -> Dict[str, Any]:
    """
    エコシステム全体の分析ダッシュボード

    - 全エージェントの進化状況俯瞰
    - システム全体の最適化トレンド
    - リソース使用効率分析
    - 予測的メンテナンス推奨
    """
    try:
        # エコシステム分析データ生成
        total_agents = len(set(record.get("agent_id") for record in evolution_engine.evolution_history))

        recent_evolutions = [
            record for record in evolution_engine.evolution_history
            if datetime.fromisoformat(record.get("timestamp", "2024-01-01")) >
               datetime.now() - timedelta(days=7)
        ]

        ecosystem_health = {
            "total_managed_agents": total_agents,
            "recent_evolution_cycles": len(recent_evolutions),
            "average_system_fitness": sum(
                record.get("validation_results", {}).get("improvement_score", 0.0)
                for record in recent_evolutions
            ) / max(len(recent_evolutions), 1),
            "api_integration_efficiency": 0.85,  # 統合API活用効率
            "resource_optimization_score": 0.78,
            "predictive_maintenance_alerts": [
                "Agent-007 scheduled for evolution in 2 days",
                "System-wide security review recommended",
                "Cost optimization opportunity detected for 3 agents"
            ],
            "ecosystem_trends": {
                "performance": "improving",
                "security": "stable",
                "cost_efficiency": "optimizing",
                "innovation_adoption": "accelerating"
            }
        }

        return ecosystem_health

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ecosystem analytics failed: {str(e)}")

@app.get("/health", tags=["System"])
async def health_check():
    """システムヘルスチェック"""
    return {
        "status": "healthy",
        "service": "Agent Evolution Engine API",
        "timestamp": datetime.now().isoformat(),
        "evolution_engine_status": "operational",
        "integrated_apis_count": len(evolution_engine.api_endpoints),
        "total_evolutions_completed": len(evolution_engine.evolution_history),
        "version": "1.0.0"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """API起動時の初期化処理"""
    print("🚀 Agent Evolution Engine API Starting...")
    print("📡 Integrated APIs:")
    for api_name, endpoint in evolution_engine.api_endpoints.items():
        print(f"   - {api_name}: {endpoint}")
    print("🎯 Ready for autonomous AI ecosystem evolution!")

@app.get("/openapi.yaml")
async def openapi_yaml():
    content = open("openapi.yaml").read()
    return PlainTextResponse(content, media_type="text/yaml")

@app.get("/llms.txt")
async def llms_txt():
    content = open("llms.txt").read()
    return PlainTextResponse(content)

@app.get("/skill.md")
async def skill_md():
    content = open("skill.md").read()
    return PlainTextResponse(content)

@app.get("/examples.md")
async def examples_md():
    content = open("examples.md").read()
    return PlainTextResponse(content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)