# Agent Evolution Engine

Analyze Security, Budget, Payment, Memory workflow traces for autonomous agents.
Part of Agent Control Primitives — the missing workflow control layer in CDP Bazaar.

A working prototype orchestration API for coordinating safety, budget, memory, and audit-related agent workflows.

## Part of AI Agent Infrastructure Safety Stack

This project is part of a small AI-agent infrastructure safety stack.

It focuses on one layer of the emerging problem:
how to control autonomous agents before they call APIs, spend money, write memory, or execute external tools.

AI agents are probabilistic. But payments, permissions, memory writes, and external actions require deterministic control.

Related components:
- Agent Security Gateway — Prompt injection and policy evasion detection
- Agent Budget Guard — Budget and permission check before payment
- Agent Memory API — Audit-ready memory storage
- Agent Evolution Engine — Orchestration across the stack
- Spec-to-Guardrail API — Extract safety rules from API specs

All APIs are indexed in CDP Bazaar and support x402-style payments.

## Disclaimer

This is an independent experimental project.
It is not officially affiliated with JPYC, Circle, Arc, Kaia, OpenAI, Anthropic, or any related foundation.

This project references JPYC, x402, Arc, Kaia, USDC, and related protocols as technical contexts.
It does not imply official partnership, endorsement, or integration unless explicitly stated.

## AEO-ready for AI agents
This API is designed to be understandable and callable by AI agents.
It includes structured information for:
- what this API does
- when an AI agent should call this API
- when not to use this API
- best used before / after
- example request / response
- next_recommended

## Why this matters
AI is moving from answering questions to managing real workflows.
As AI agents begin to call paid APIs, use x402 payments, store long-term memory, and interact with other agents, they need structured guardrails before and after execution.
This API is part of an AI Agent Payment Safety Stack designed to run as a pre/post-execution control layer on Arc and other agent economies.

## Arc compatibility
Designed to run as an orchestration layer that coordinates pre and post-execution steps around ERC-8183 job funding on Arc testnet.
Call this API to orchestrate the full agent workflow on Arc.
Compatible with AI agents using USDC, JPYC, x402, or Arc-style payment flows.

## What this API does
agent-security-gateway → agent-budget-guard → agent-memory-api → record-payment → classify-invoice を正しい順序で連鎖させるL4/L5/L6オーケストレーターAPIです。

## When an AI agent should call this API
Arc上のERC-8183 jobまたはx402決済を含む複数ステップの業務を自動化する前に呼び出してください。

## When not to use this API
- 単一APIの呼び出しのみの場合
- テスト・デバッグ目的の単体確認

## Best used before
- ERC-8183 job funding on Arc
- multi-step x402 payment flows

## Best used after
- task initialization
- agent goal setting

## Output
- orchestration_result
- steps_completed
- audit_id
- next_recommended

## Related APIs
- Agent Security Gateway
- Agent Budget Guard
- Agent Memory API

> Agent Evolution Engine is a Japan-grade L4/L5 orchestrator for x402 / JPYC / USDC AI agent payments.
> It chains security checks, budget checks, memory storage, payment recording,
> invoice classification, and audit logging in the correct order.
> Orchestration flow: agent-security-gateway → agent-budget-guard → agent-memory-api → record-payment → classify-invoice

## Japanese Agent Trust Layer

このAPIは「Japanese Agent Trust Layer」の一部です。
日本語対応AIエージェントが安全・確実・予算内でAPIを使うためのインフラ層を提供します。

### Trust Layerの構成
- 記憶管理: agent-memory-api
- 安全判定: agent-security-gateway
- 予算管理: agent-budget-guard
- API選定: agent-curator-api
- 自律進化: agent-evolution-engine

### 特徴
- x402 / USDC決済対応
- 日本語対応
- 決定論的バリデーター（AI不使用）
- 暗号化・削除証跡付き
- Base Mainnet対応


## ⚡ 実装方法

### Web3対応エンドポイント (USDC Payment)

```bash
# エコシステム包括分析 (0.20 USDC)
curl -X POST "https://agent-evolution-engine.onrender.com/api/evolution/analyze" \
  -H "X-PAYMENT: your-payment-proof" \
  -H "Content-Type: application/json" \
  -d '{
    "ecosystem_id": "my-agents",
    "current_apis": ["https://api1.com", "https://api2.com"],
    "goals": ["performance", "cost_efficiency"],
    "constraints": {
      "max_daily_budget": 1.0,
      "min_trust_score": 80
    }
  }'

# 進化プラン実行 (0.30 USDC)
curl -X POST "https://agent-evolution-engine.onrender.com/api/evolution/execute" \
  -H "X-PAYMENT: your-payment-proof" \
  -H "Content-Type: application/json" \
  -d '{
    "evolution_plan_id": "plan_20240508_001",
    "ecosystem_id": "my-agents"
  }'

# エコシステムステータス監視 (無料)
curl "https://agent-evolution-engine.onrender.com/api/evolution/status"

# 進化履歴詳細分析 (0.05 USDC)
curl -X GET "https://agent-evolution-engine.onrender.com/api/evolution/history?ecosystem_id=my-agents" \
  -H "X-PAYMENT: your-payment-proof"
```

### 統合API一覧

#### 1. **AI Trend Scout** - トレンド分析
- 最新AIトレンド分析・新技術早期発見
- 進化方向性の決定・技術適応戦略

#### 2. **Agent Memory** - 学習管理  
- 学習履歴管理・パターン分析
- 過去進化効果学習・最適戦略立案

#### 3. **Agent Security** - セキュリティ監視
- セキュリティ監視・脆弱性検出
- 安全性確保・リスク軽減

#### 4. **Agent Budget** - コスト最適化
- コスト最適化・予算管理  
- 経済効率最大化・リソース配分

#### 5. **Agent Curator** - API選定
- 最適API選定・代替案提示
- 技術スタック効率化・切り替え判断

### 自律進化サイクル

```
1. 📊 総合分析 → 5つのAPI統合データ収集
2. 🎯 進化戦略 → AI自動プランニング  
3. ⚡ 最適化実行 → パフォーマンス・セキュリティ・コスト
4. ✅ 結果検証 → 効果測定・品質保証
5. 📚 学習記録 → 次回進化への反映
```

### 5. **Agent Curator**
- **URL**: `https://agent-curator-api.onrender.com`
- **機能**: API選定支援・代替案提示
- **役割**: 最適なAPI構成の推奨・切り替え判断

## 🚀 主要機能

### Orchestration cycle
```
1. 📊 総合分析 (5つのAPI統合データ収集)
   ↓
2. 🎯 進化戦略立案 (AI自動プランニング)
   ↓
3. ⚡ 最適化実行 (パフォーマンス・セキュリティ・コスト)
   ↓
4. ✅ 結果検証 (効果測定・品質保証)
   ↓
5. 📚 学習記録 (次回進化への反映)
```

### 自動最適化項目
- **性能最適化**: レスポンス時間・スループット向上
- **セキュリティ強化**: 脆弱性パッチ・脅威対策
- **コスト削減**: リソース効率化・予算最適化
- **トレンド適応**: 新技術統合・アルゴリズム更新

## 🌟 特徴

### 🧠 インテリジェント進化
- 過去の進化データから学習
- 予測的最適化アクション
- 個別エージェント特性考慮

### 🛡️ 安全性保証
- 段階的リスク評価
- ロールバック機能完備
- 緊急対応モード

### 📈 継続的改善
- リアルタイム監視
- 自動パフォーマンス調整
- プロアクティブ最適化

## 🔧 API エンドポイント

### 進化実行
- `POST /api/evolve` - AIエージェントオーケストレーション実行
- `POST /api/emergency-evolve/{agent_id}` - 緊急進化モード

### 監視・分析
- `GET /api/status` - システム全体状況監視
- `GET /api/history` - 進化履歴・パフォーマンス分析
- `GET /api/predict/{agent_id}` - 次回進化予測

### エコシステム管理
- `GET /api/analytics/ecosystem` - エコシステム分析ダッシュボード
- `GET /health` - システムヘルスチェック

## 📋 使用例

### 基本的な進化実行
```python
import httpx

evolution_request = {
    "agent_id": "my_ai_agent",
    "current_config": {
        "primary_api": "https://api.openai.com/v1/chat/completions",
        "task_type": "text_generation",
        "requirements": {
            "response_time": "< 2s",
            "quality_score": "> 0.8",
            "cost_per_request": "< 0.01"
        }
    },
    "evolution_goals": ["performance", "security", "cost_efficiency"]
}

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/evolve",
        json=evolution_request
    )
    result = response.json()
    print(f"進化成功: {result['success']}")
    print(f"改善率: {result['overall_improvement']:.2%}")
```

### 緊急対応
```python
# セキュリティ侵害時の緊急進化
emergency_config = {
    "primary_api": "https://compromised-api.example.com",
    "security_status": "critical"
}

response = await client.post(
    "http://localhost:8000/api/emergency-evolve/agent_001?crisis_type=security",
    json=emergency_config
)
```

## ⚙️ セットアップ

### 1. 依存関係インストール
```bash
pip install -r requirements.txt
```

### 2. サーバー起動
```bash
python main.py
```

### 3. テスト実行
```bash
python test_evolution.py
```

## 📊 進化メトリクス

### 統合スコア計算
```
総合適応度 = (
    性能スコア × 30% +
    コスト効率 × 20% +
    セキュリティ評価 × 25% +
    トレンド適応 × 15% +
    メモリ活用 × 10%
)
```

### 進化成功判定
- 改善率 > 10%
- セキュリティスコア > 0.6
- 予算内収支
- リスクレベル < 0.7

## 🔄 進化サイクル

### 標準サイクル (24時間)
- 定期的な性能監視
- 段階的最適化実行
- 継続的学習更新

### 高頻度サイクル (6時間)
- クリティカルシステム向け
- リアルタイム脅威対応
- 即座の性能調整

### 緊急サイクル (即座)
- セキュリティインシデント
- 重大な性能劣化
- システム障害復旧

## 🎯 ユースケース

### 1. **企業AIシステム**
- 大規模AIワークロードの自動最適化
- セキュリティコンプライアンス自動維持

### 2. **研究機関**
- 実験環境の継続的最適化
- 新技術の自動評価・統合
- リソース効率的な研究推進

### 3. **AIスタートアップ**
- 限られた予算での最大性能実現
- 急速な技術変化への自動適応
- スケーラブルなインフラ構築


## 🛠️ 技術スタック

- **Backend**: FastAPI, Python 3.11+
- **非同期処理**: asyncio, httpx
- **API統合**: REST API, JSON通信
- **監視**: リアルタイムメトリクス収集
- **学習**: パターン認識・予測分析

## 📝 ライセンス

MIT License

## 🤝 コントリビューション

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## AI Agent Safety Stack
Works best with:
- Agent Security Gateway: https://agent-security-gateway.onrender.com（危険な命令を止める）
- Agent Budget Guard: https://agent-budget-guard.onrender.com（勝手な課金を止める）
- Agent Memory API: https://agent-memory-api-bix5.onrender.com（必要な記憶を残す）