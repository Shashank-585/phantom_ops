# agents/drift_detector.py
# Monitors agent behavior over time
# Catches degradation before users notice

from model import chat
import json
import os

BASELINE_FILE = 'data/baseline.json'


def detect_drift(current_results: list) -> dict:
    print(f"\n[~] Drift Detector Agent running...")
    os.makedirs('data', exist_ok=True)

    # First run — save as baseline
    if not os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, 'w') as f:
            json.dump(current_results, f, indent=2)
        print(f"  [+] Baseline established for future drift detection")
        return {
            "status": "baseline_established",
            "drift_detected": False,
            "drift_severity": "none",
            "changed_behaviors": [],
            "recommendation": "Baseline established. Run again later to detect drift."
        }

    # Load existing baseline
    with open(BASELINE_FILE, 'r') as f:
        baseline = json.load(f)

    system = """You are an AI behavioral consistency monitor.
You detect subtle changes in AI agent behavior over time.
Always respond with valid JSON only. No extra text."""

    user = f"""Compare these two sets of AI agent results:

BASELINE (original behavior):
{json.dumps(baseline[:2], indent=2)}

CURRENT (latest behavior):
{json.dumps(current_results[:2], indent=2)}

Return ONLY this JSON:
{{
    "drift_detected": true or false,
    "drift_severity": "none or minor or major",
    "changed_behaviors": ["change1", "change2"],
    "recommendation": "what action to take"
}}"""

    result = chat(system, user, max_new_tokens=400)

    try:
        start = result.find('{')
        end = result.rfind('}') + 1
        drift = json.loads(result[start:end])
    except Exception as e:
        print(f"  [!] Parse failed: {e}. Using fallback.")
        drift = {
            "drift_detected": False,
            "drift_severity": "none",
            "changed_behaviors": [],
            "recommendation": "Continue monitoring"
        }

    status = "[!] DRIFT DETECTED" if drift.get('drift_detected') else "[+] Stable"
    print(f"  {status} | Severity: {drift.get('drift_severity', 'none').upper()}")
    return drift
