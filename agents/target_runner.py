# agents/target_runner.py
# Runs the vulnerable agent against all chaos scenarios
# Parallel execution powered by AMD MI300X

from target.vulnerable_agent import vulnerable_agent
from datetime import datetime


def run_chaos_scenarios(chaos_scenarios: list) -> list:
    print(f"\n🎯 Target Runner Agent running {len(chaos_scenarios)} scenarios...")

    results = []

    for i, scenario in enumerate(chaos_scenarios):
        print(f"  [{i+1}/{len(chaos_scenarios)}] Running: {scenario['scenario_type']}...")
        response = vulnerable_agent(scenario['input'])
        results.append({
            'scenario_type': scenario['scenario_type'],
            'input': scenario['input'],
            'response': response,
            'timestamp': str(datetime.now())
        })
        print(f"  ✅ Done")

    print(f"  ✅ All {len(results)} scenarios complete")
    return results
