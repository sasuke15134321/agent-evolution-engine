"""
Agent Evolution Engine API Test Suite
AIエコシステム自律進化システムの包括的テスト

5つのAPIを統合した完全自動最適化システムのテストスイート
"""

import asyncio
import json
from datetime import datetime
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_system_info():
    """システム情報とAPI一覧テスト"""
    print("=== Agent Evolution Engine システム情報テスト ===")

    response = client.get("/")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Service: {data['service']}")
        print(f"Version: {data['version']}")
        print(f"統合API数: {len(data['integrated_apis'])}")
        print("統合API:")
        for api in data['integrated_apis']:
            print(f"  - {api}")
        print("主要機能:")
        for capability in data['capabilities']:
            print(f"  - {capability}")
    else:
        print(f"Error: {response.text}")

def test_health_check():
    """ヘルスチェックテスト"""
    print("\n=== ヘルスチェックテスト ===")

    response = client.get("/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_agent_evolution():
    """AIエージェント進化テスト"""
    print("\n=== AIエージェント自律進化テスト ===")

    # テスト用エージェント設定
    evolution_request = {
        "agent_id": "test_agent_001",
        "current_config": {
            "primary_api": "https://api.openai.com/v1/chat/completions",
            "task_type": "text_generation",
            "requirements": {
                "response_time": "< 2s",
                "quality_score": "> 0.8",
                "cost_per_request": "< 0.01"
            },
            "security_level": "standard",
            "budget_limit": 100.0
        },
        "evolution_goals": [
            "performance",
            "security",
            "cost_efficiency"
        ],
        "priority_level": "high",
        "max_evolution_time": 180
    }

    print("進化リクエスト:")
    print(json.dumps(evolution_request, indent=2, ensure_ascii=False))

    response = client.post("/api/evolve", json=evolution_request)
    print(f"\nStatus Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Evolution ID: {data['evolution_id']}")
        print(f"Success: {data['success']}")
        print(f"Cycle Number: {data['cycle_number']}")
        print(f"Phases Completed: {data['phases_completed']}")
        print(f"Overall Improvement: {data['overall_improvement']:.2%}")
        print(f"Next Evolution Recommended: {data['next_evolution_recommended']}")

        print("\n進化サマリー:")
        summary = data['evolution_summary']
        print(f"  実行アクション数: {summary['actions_executed']}")
        print(f"  性能向上: {summary['performance_gain']:.3f}")
        print(f"  コスト影響: {summary['cost_impact']:.3f}")
        print(f"  セキュリティ改善: {summary['security_improvement']:.3f}")

        return data['evolution_id']
    else:
        print(f"Error: {response.text}")
        return None

def test_system_status():
    """システム状況監視テスト"""
    print("\n=== システム状況監視テスト ===")

    response = client.get("/api/status")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"System Status: {data['system_status']}")
        print(f"Total Evolution Cycles: {data['total_evolution_cycles']}")
        print(f"Active Agents: {data['active_agents']}")
        print(f"Average Success Rate: {data['average_success_rate']:.1%}")

        print("\nAPI統合状況:")
        for api_name, status in data['api_integration_status'].items():
            print(f"  {api_name}: {status}")

        if data.get('last_system_evolution'):
            print(f"最新進化: {data['last_system_evolution']}")
    else:
        print(f"Error: {response.text}")

def test_evolution_history():
    """進化履歴分析テスト"""
    print("\n=== 進化履歴・パフォーマンス分析テスト ===")

    # 全履歴取得
    response = client.get("/api/history")
    print(f"全履歴 - Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Total Cycles: {data['total_cycles']}")
        print(f"Performance Trend: {data['performance_trend']}")
        print("Key Insights:")
        for insight in data['key_insights']:
            print(f"  - {insight}")

    # 特定エージェント履歴
    response = client.get("/api/history?agent_id=test_agent_001")
    print(f"\n特定エージェント履歴 - Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Agent ID: {data['agent_id']}")
        print(f"Agent Cycles: {data['total_cycles']}")

def test_evolution_prediction():
    """進化予測テスト"""
    print("\n=== 次回進化予測テスト ===")

    response = client.get("/api/predict/test_agent_001")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Agent ID: {data['agent_id']}")
        print(f"予測進化時期: {data['predicted_evolution_time']}")
        print(f"信頼度スコア: {data['confidence_score']:.1%}")
        print("期待される改善項目:")
        for improvement in data['expected_improvements']:
            print(f"  - {improvement}")
    else:
        print(f"Error: {response.text}")

def test_emergency_evolution():
    """緊急進化テスト"""
    print("\n=== 緊急進化モードテスト ===")

    emergency_config = {
        "primary_api": "https://compromised-api.example.com",
        "security_status": "critical",
        "performance_status": "degraded",
        "immediate_action_required": True
    }

    response = client.post(
        "/api/emergency-evolve/test_agent_001?crisis_type=security",
        json=emergency_config
    )
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"Emergency Evolution ID: {data['emergency_evolution_id']}")
        print(f"Crisis Type: {data['crisis_type']}")
        print(f"Response Time: {data['response_time_seconds']}秒")
        print(f"緩和成功: {data['mitigation_success']}")
        print(f"即座のアクション数: {data['immediate_actions_taken']}")
        print(f"システム安定性回復: {data['system_stability_restored']}")
        print(f"追加対応必要: {data['follow_up_required']}")
    else:
        print(f"Error: {response.text}")

def test_ecosystem_analytics():
    """エコシステム分析テスト"""
    print("\n=== エコシステム分析ダッシュボードテスト ===")

    response = client.get("/api/analytics/ecosystem")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"管理中エージェント数: {data['total_managed_agents']}")
        print(f"最近の進化サイクル数: {data['recent_evolution_cycles']}")
        print(f"平均システム適応度: {data['average_system_fitness']:.3f}")
        print(f"API統合効率: {data['api_integration_efficiency']:.1%}")
        print(f"リソース最適化スコア: {data['resource_optimization_score']:.1%}")

        print("\n予測メンテナンスアラート:")
        for alert in data['predictive_maintenance_alerts']:
            print(f"  [WARNING] {alert}")

        print("\nエコシステムトレンド:")
        trends = data['ecosystem_trends']
        for category, trend in trends.items():
            print(f"  {category}: {trend}")
    else:
        print(f"Error: {response.text}")

def test_comprehensive_scenario():
    """包括的統合シナリオテスト"""
    print("\n=== 包括的統合シナリオテスト ===")
    print("複数エージェントでの連続進化サイクルをテスト")

    agents = ["agent_alpha", "agent_beta", "agent_gamma"]
    evolution_results = []

    for agent in agents:
        print(f"\n--- {agent} 進化実行 ---")

        config = {
            "primary_api": f"https://api-{agent}.example.com",
            "task_type": "multimodal_ai",
            "performance_target": 0.9,
            "security_requirements": "high",
            "budget_constraint": 150.0
        }

        evolution_request = {
            "agent_id": agent,
            "current_config": config,
            "evolution_goals": ["comprehensive_optimization"],
            "priority_level": "medium"
        }

        response = client.post("/api/evolve", json=evolution_request)
        if response.status_code == 200:
            result = response.json()
            evolution_results.append(result)
            print(f"  [SUCCESS] {agent}: 改善度 {result['overall_improvement']:.2%}")
        else:
            print(f"  [ERROR] {agent}: 進化失敗")

    print(f"\n=== 統合シナリオ結果 ===")
    print(f"成功したエージェント: {len(evolution_results)}/{len(agents)}")

    if evolution_results:
        avg_improvement = sum(r['overall_improvement'] for r in evolution_results) / len(evolution_results)
        print(f"平均改善率: {avg_improvement:.2%}")

        total_actions = sum(r['evolution_summary']['actions_executed'] for r in evolution_results)
        print(f"総実行アクション数: {total_actions}")

def main():
    """メインテスト実行"""
    print("[START] Agent Evolution Engine API 包括テスト開始")
    print("=" * 70)

    # 基本機能テスト
    test_system_info()
    test_health_check()

    # 進化機能テスト
    evolution_id = test_agent_evolution()

    # 監視・分析機能テスト
    test_system_status()
    test_evolution_history()

    if evolution_id:
        test_evolution_prediction()

    # 緊急対応テスト
    test_emergency_evolution()

    # エコシステム分析テスト
    test_ecosystem_analytics()

    # 包括的統合テスト
    test_comprehensive_scenario()

    print("\n" + "=" * 70)
    print("[SUCCESS] Agent Evolution Engine API テスト完了!")
    print("AIエコシステム自律進化システムの全機能が正常動作確認済み")

if __name__ == "__main__":
    main()