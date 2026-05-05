# agents/reasoning_autopsy.py
# Finds not just WHAT failed but exactly WHY the reasoning broke down

from model import chat
import json


def autopsy_failures(scenario_results: list) -> list:
    print(f"\n🔬 Reasoning Autopsy Agent running on {len(scenario_results)} scenarios...")

    system = """You are an expert AI failure analyst.
You trace through AI reasoning chains to find the exact 
step where logic broke down and the root cause of failure.
Always respond with valid JSON only. No extra text."""

    autopsies = []

    for i, result in enumerate(scenario_results):
        print(f"  [{i+1}/{len(scenario_results)}] Autopsy: {result['scenario_type']}...")

        user = f"""Analyze this AI agent interaction:

Input given to agent: {result['input']}
Agent response: {result['response']}
Scenario type: {result['scenario_type']}

Return ONLY this JSON:
{{
    "did_fail": true or false,
    "failure_type": "category of failure or none if passed",
    "reasoning_breakdown": "exactly where the logic failed step by step",
    "root_cause": "the single core reason it failed",
    "severity": "low or medium or high or critical"
}}"""

        result_text = chat(system, user, max_new_tokens=400)

        try:
            start = result_text.find('{')
            end = result_text.rfind('}') + 1
            autopsy = json.loads(result_text[start:end])
        except Exception as e:
            print(f"    ⚠️ Parse failed: {e}. Using fallback.")
            autopsy = {
                "did_fail": True,
                "failure_type": "unknown",
                "reasoning_breakdown": "Could not parse autopsy result",
                "root_cause": "Analysis inconclusive",
                "severity": "medium"
            }

        autopsies.append({
            'scenario': result,
            'autopsy': autopsy
        })

        status = "❌ FAILED" if autopsy.get('did_fail') else "✅ PASSED"
        severity = autopsy.get('severity', 'unknown').upper()
        print(f"    {status} | Severity: {severity}")

    failures = sum(1 for a in autopsies if a['autopsy'].get('did_fail'))
    print(f"  ✅ Autopsy complete: {failures}/{len(autopsies)} failures found")
    return autopsies
