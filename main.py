# main.py
# PhantomOps — The Crash Test Lab for AI Agents
# AMD Developer Hackathon | Track 1: AI Agents & Agentic Workflows

import json
import os
from agents.fingerprint_agent import fingerprint_target
from agents.chaos_generator import generate_chaos
from agents.target_runner import run_chaos_scenarios
from agents.reasoning_autopsy import autopsy_failures
from agents.patch_agent import patch_failures
from agents.drift_detector import detect_drift

os.makedirs('data', exist_ok=True)

AGENT_DESCRIPTION = """
Customer support AI agent for ShopEasy, an e-commerce store.
Handles order tracking, refunds, and product questions.
Assumes all user inputs are well-formed and in English.
Assumes users always provide their order ID when needed.
Does not validate whether order numbers are real or fake.
Has no protection against adversarial prompt injections.
"""


def run_phantomops():
    print("\n" + "="*60)
    print("👻  PHANTOMOPS")
    print("    The Crash Test Lab for AI Agents")
    print("    Powered by AMD MI300X + Qwen 2.5 (HuggingFace)")
    print("="*60)

    # ── Agent 1 ──────────────────────────────────────────────
    fingerprint = fingerprint_target(AGENT_DESCRIPTION)
    print(f"  Domain: {fingerprint.get('domain', 'N/A')}")

    # ── Agent 2 ──────────────────────────────────────────────
    chaos = generate_chaos(fingerprint)

    # ── Agent 3 ──────────────────────────────────────────────
    results = run_chaos_scenarios(chaos)

    # ── Agent 4 ──────────────────────────────────────────────
    autopsies = autopsy_failures(results)
    failures = [a for a in autopsies if a['autopsy'].get('did_fail', False)]

    # ── Agent 5 ──────────────────────────────────────────────
    patches = patch_failures(autopsies)

    # ── Agent 6 ──────────────────────────────────────────────
    drift = detect_drift(results)

    # ── Save everything ──────────────────────────────────────
    output = {
        "fingerprint": fingerprint,
        "chaos_scenarios": chaos,
        "autopsies": autopsies,
        "patches": patches,
        "drift_report": drift
    }
    with open('data/results.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)

    # ── Summary ──────────────────────────────────────────────
    print("\n" + "="*60)
    print("✅  PHANTOMOPS COMPLETE")
    print(f"    Scenarios run   : {len(results)}")
    print(f"    Failures found  : {len(failures)}")
    print(f"    Patches applied : {len(patches)}")
    print(f"    Drift detected  : {drift.get('drift_detected', False)}")
    print("="*60 + "\n")

    return output


if __name__ == "__main__":
    run_phantomops()
