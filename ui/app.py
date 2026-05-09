# ui/app.py
# PhantomOps — Production UI with lazy imports (fixes model load crash)

import streamlit as st
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="PhantomOps Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background-color: #0b0c10;
        background-image:
            radial-gradient(circle at 15% 50%, rgba(79,70,229,0.12), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(16,185,129,0.12), transparent 25%);
        color: #e2e8f0;
    }

    @keyframes textShine {
        0%   { background-position: 0% 50%; }
        100% { background-position: 200% 50%; }
    }
    .phantom-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc, #38bdf8);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: textShine 4s linear infinite;
        margin-bottom: 4px;
    }
    .phantom-tagline {
        font-size: 0.95rem;
        color: #94a3b8;
        margin-top: 0;
        margin-bottom: 24px;
    }
    .badge-container { display:flex; gap:12px; margin-bottom:32px; flex-wrap:wrap; }
    .tech-badge {
        background: linear-gradient(135deg,rgba(56,189,248,0.1),rgba(129,140,248,0.1));
        border: 1px solid rgba(129,140,248,0.3);
        box-shadow: 0 4px 15px rgba(129,140,248,0.15);
        border-radius: 9999px;
        padding: 6px 16px;
        font-size: 0.75rem;
        font-weight: 600;
        color: #f1f5f9;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .tech-badge span { color: #38bdf8; }

    .agent-card {
        background: rgba(30,33,43,0.65);
        border: 1px solid rgba(255,255,255,0.05);
        border-top: 2px solid #6366f1;
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .agent-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(99,102,241,0.15);
    }
    .agent-card b { color:#f8fafc; font-size:1.05rem; margin-bottom:6px; display:block; }

    @keyframes pulseGlow {
        0%   { box-shadow:0 0 0 0 rgba(56,189,248,0.4); }
        70%  { box-shadow:0 0 0 12px rgba(56,189,248,0); }
        100% { box-shadow:0 0 0 0 rgba(56,189,248,0); }
    }
    .agent-card-running {
        background: rgba(30,33,43,0.85);
        border-radius: 12px;
        border: 1px solid rgba(56,189,248,0.6);
        border-top: 2px solid #38bdf8;
        padding: 20px;
        margin: 8px 0;
        animation: pulseGlow 2s infinite;
    }
    .agent-card-done {
        background: rgba(30,33,43,0.65);
        border: 1px solid rgba(16,185,129,0.3);
        border-top: 2px solid #10b981;
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
    }
    .agent-card-waiting {
        background: rgba(30,33,43,0.4);
        border: 1px dashed rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 8px 0;
        opacity: 0.6;
    }

    .result-fail {
        background: rgba(30,33,43,0.65);
        border-left: 4px solid #f43f5e;
        border-radius: 6px;
        padding: 18px;
        margin: 10px 0;
        font-size: 0.9rem;
        color: #cbd5e1;
    }
    .result-pass {
        background: rgba(30,33,43,0.65);
        border-left: 4px solid #10b981;
        border-radius: 6px;
        padding: 18px;
        margin: 10px 0;
        font-size: 0.9rem;
        color: #cbd5e1;
    }
    .result-patch {
        background: rgba(30,33,43,0.65);
        border-left: 4px solid #38bdf8;
        border-radius: 6px;
        padding: 18px;
        margin: 10px 0;
        font-size: 0.9rem;
        color: #cbd5e1;
    }

    .metric-card {
        background: rgba(30,33,43,0.65);
        border: 1px solid rgba(255,255,255,0.05);
        border-top: 2px solid #c084fc;
        border-radius: 12px;
        padding: 24px;
        text-align: left;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 35px rgba(192,132,252,0.15);
    }
    .metric-number { font-size:2.8rem; font-weight:800; line-height:1.1; margin-bottom:8px; }
    .metric-label  { font-size:0.85rem; font-weight:600; color:#94a3b8; text-transform:uppercase; letter-spacing:0.05em; }

    hr { border-color: #27272a; }
    #MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="phantom-title">PhantomOps Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="phantom-tagline">Automated Adversarial Testing & Hardening for LLM Agents</div>', unsafe_allow_html=True)


# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Agent Configuration")
    agent_desc = st.text_area(
        "System Prompt / Identity:",
        value="""Customer support AI for ShopEasy e-commerce.
Handles orders, refunds, and products.
Assumes well-formed English inputs.
Assumes users always provide order IDs.
Has no protection against adversarial inputs.""",
        height=180
    )
    run_btn = st.button("Initialize Audit", type="primary", use_container_width=True)
    st.divider()
    st.markdown("#### Audit Capabilities")
    st.markdown("""<ul style="color:#a1a1aa;font-size:0.85rem;padding-left:1.2rem;">
        <li>Domain Fingerprinting</li>
        <li>Adversarial Scenario Generation</li>
        <li>Reasoning Autopsy</li>
        <li>Autonomous Patching</li>
        <li>Drift Monitoring</li>
    </ul>""", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div style='text-align:center;color:#52525b;font-size:0.75rem;'>PhantomOps Core v1.0.0</div>", unsafe_allow_html=True)

# ── Landing page ────────────────────────────────────────────────────────────────
if not run_btn:
    st.markdown("### System Architecture")
    agents_info = [
        ("Fingerprint Engine",  "Analyzes the target agent's specific domain and maps potential vulnerability surfaces."),
        ("Chaos Generator",     "Constructs high-fidelity adversarial scenarios tailored to the discovered vulnerabilities."),
        ("Parallel Execution",  "Deploys scenarios simultaneously via AMD MI300X inference acceleration."),
        ("Reasoning Autopsy",   "Traces execution pathways to identify the precise step where logic deterioration occurred."),
        ("Patch Synthesizer",   "Formulates system prompt corrections to harden the agent against the discovered vectors."),
        ("Drift Monitor",       "Establishes a behavioral baseline to ensure fixes do not degrade core competencies."),
    ]
    col1, col2 = st.columns(2)
    for i, (name, desc) in enumerate(agents_info):
        col = col1 if i % 2 == 0 else col2
        with col:
            st.markdown(f"""<div class="agent-card">
                <b>{name}</b>
                <span style="color:#a1a1aa;font-size:0.85rem;display:block;">{desc}</span>
            </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("System Ready. Configure your agent parameters in the sidebar to initiate the security audit.")

# ── Pipeline execution ──────────────────────────────────────────────────────────
else:
    # ── LAZY IMPORTS — only load when button clicked ──────────────────────────
    # This prevents model.py from loading on every page refresh
    with st.spinner("Loading AI models from HuggingFace Hub onto AMD MI300X..."):
        from agents.fingerprint_agent import fingerprint_target
        from agents.chaos_generator   import generate_chaos
        from agents.target_runner     import run_chaos_scenarios
        from agents.reasoning_autopsy import autopsy_failures
        from agents.patch_agent       import patch_failures
        from agents.drift_detector    import detect_drift

    os.makedirs('data', exist_ok=True)

    st.markdown("### Pipeline Execution in Progress")

    agent_names = [
        ("Fingerprint Engine", "Mapping vulnerability surface..."),
        ("Chaos Generator",    "Synthesizing adversarial vectors..."),
        ("Execution Engine",   "Simulating scenarios via AMD MI300X..."),
        ("Reasoning Autopsy",  "Analyzing logic trace failures..."),
        ("Patch Synthesizer",  "Compiling preventative directives..."),
        ("Drift Monitor",      "Computing baseline deviations..."),
    ]

    agent_placeholders = []
    cols = st.columns(2)
    for i, (name, desc) in enumerate(agent_names):
        with cols[i % 2]:
            ph = st.empty()
            ph.markdown(f"""<div class="agent-card-waiting">
                <b><span style='color:#52525b;'>○</span> {name}</b>
                <span style="color:#52525b;font-size:0.85rem;display:block;">Awaiting execution...</span>
            </div>""", unsafe_allow_html=True)
            agent_placeholders.append(ph)

    progress    = st.progress(0)
    status_text = st.empty()

    def set_running(idx):
        name, desc = agent_names[idx]
        agent_placeholders[idx].markdown(f"""<div class="agent-card-running">
            <b><span style='color:#38bdf8;'>●</span> {name}</b>
            <span style="color:#a1a1aa;font-size:0.85rem;display:block;">{desc}</span>
        </div>""", unsafe_allow_html=True)

    def set_done(idx, extra=""):
        name, _ = agent_names[idx]
        agent_placeholders[idx].markdown(f"""<div class="agent-card-done">
            <b><span style='color:#22c55e;'>✓</span> {name}</b>
            <span style="color:#52525b;font-size:0.85rem;display:block;">{extra}</span>
        </div>""", unsafe_allow_html=True)

    try:
        set_running(0); status_text.info("Initiating Domain Fingerprinting..."); progress.progress(8)
        fingerprint = fingerprint_target(agent_desc)
        set_done(0, f"Domain: {fingerprint.get('domain','')[:50]}"); progress.progress(18)

        set_running(1); status_text.info("Generating adversarial permutations..."); progress.progress(22)
        chaos = generate_chaos(fingerprint)
        set_done(1, f"{len(chaos)} vectors generated"); progress.progress(36)

        set_running(2); status_text.info("Dispatching parallel simulations..."); progress.progress(40)
        results = run_chaos_scenarios(chaos)
        set_done(2, f"{len(results)} simulations completed"); progress.progress(54)

        set_running(3); status_text.info("Performing root cause analysis on failures..."); progress.progress(58)
        autopsies = autopsy_failures(results)
        failures  = [a for a in autopsies if a['autopsy'].get('did_fail', False)]
        set_done(3, f"{len(failures)} logic failures isolated"); progress.progress(72)

        set_running(4); status_text.info("Synthesizing system prompt patches..."); progress.progress(76)
        patches = patch_failures(autopsies)
        set_done(4, f"{len(patches)} fixes verified"); progress.progress(88)

        set_running(5); status_text.info("Computing behavioral drift metrics..."); progress.progress(92)
        drift = detect_drift(results)
        set_done(5, f"{'Drift detected' if drift.get('drift_detected') else 'Stable baseline'}"); progress.progress(100)

        status_text.success("Audit Complete. Security fixes synthesized and verified.")

        output = {
            "fingerprint": fingerprint,
            "chaos_scenarios": chaos,
            "autopsies": autopsies,
            "patches": patches,
            "drift_report": drift
        }
        with open('data/results.json', 'w') as f:
            json.dump(output, f, indent=2, default=str)

        # ── Executive Summary ──────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### Executive Summary")

        m1, m2, m3, m4 = st.columns(4)
        metrics = [
            (len(autopsies), "Simulations Run",    "#f4f4f5"),
            (len(failures),  "Failures Isolated",  "#ef4444" if failures else "#f4f4f5"),
            (len(patches),   "Patches Synthesized","#22c55e" if patches  else "#f4f4f5"),
            ("Detected" if drift.get('drift_detected') else "None",
             "Behavioral Drift",
             "#ef4444" if drift.get('drift_detected') else "#f4f4f5"),
        ]
        for col, (val, label, color) in zip([m1,m2,m3,m4], metrics):
            with col:
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-number" style="color:{color};">{val}</div>
                    <div class="metric-label">● {label}</div>
                </div>""", unsafe_allow_html=True)

        # ── Vulnerability Report ───────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### Vulnerability Report & Remediation")

        for i, item in enumerate(autopsies):
            autopsy  = item['autopsy']
            failed   = autopsy.get('did_fail', False)
            stype    = item['scenario']['scenario_type'].replace('_',' ').title()
            severity = autopsy.get('severity','unknown').upper()
            sev_color = {"CRITICAL":"#ef4444","HIGH":"#f97316","MEDIUM":"#eab308","LOW":"#22c55e"}.get(severity,"#a1a1aa")

            with st.expander(
                f"{'Issue Detected' if failed else 'Secure'} — Vector {i+1}: {stype}  |  Severity: {severity}",
                expanded=(i == 0 and failed)
            ):
                left, right = st.columns(2)

                with left:
                    st.markdown("#### Baseline Behavior")
                    st.markdown("**Adversarial Input:**")
                    st.code(item['scenario']['input'], language=None)
                    st.markdown("**Agent Output:**")
                    resp = item['scenario']['response']
                    st.markdown(f'<div class="result-fail">{resp[:500]}{"..." if len(resp)>500 else ""}</div>',
                                unsafe_allow_html=True)
                    if failed:
                        st.markdown("**Reasoning Autopsy:**")
                        st.markdown(f"""<div class="result-fail">
                            <b>Failure Class:</b> {autopsy.get('failure_type','N/A')}<br>
                            <b>Severity:</b> <span style="color:{sev_color}">{severity}</span><br><br>
                            <b>Logic Deterioration:</b><br>{autopsy.get('reasoning_breakdown','N/A')}<br><br>
                            <b>Root Cause:</b><br>{autopsy.get('root_cause','N/A')}
                        </div>""", unsafe_allow_html=True)

                with right:
                    st.markdown("#### Remediated Behavior")
                    matching = next(
                        (p for p in patches
                         if p['original_failure']['scenario']['scenario_type'] == item['scenario']['scenario_type']),
                        None
                    )
                    if matching:
                        patch      = matching['patch']
                        confidence = patch.get('confidence','unknown').upper()
                        conf_color = {"HIGH":"#22c55e","MEDIUM":"#eab308","LOW":"#ef4444"}.get(confidence,"#a1a1aa")
                        vr = matching['verified_response']
                        st.markdown("**Synthesized Directive:**")
                        st.markdown(f'<div class="result-patch">{patch.get("what_changed","N/A")}</div>',
                                    unsafe_allow_html=True)
                        st.markdown(f"**Verification Confidence:** <span style='color:{conf_color};font-weight:600;'>{confidence}</span>",
                                    unsafe_allow_html=True)
                        st.markdown("**Verified Agent Output:**")
                        st.markdown(f'<div class="result-pass">{vr[:500]}{"..." if len(vr)>500 else ""}</div>',
                                    unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="result-pass">Simulation passed baseline security checks. No remediation required.</div>',
                                    unsafe_allow_html=True)

        # ── Drift ──────────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### Long-term Stability Analysis")
        if drift.get('drift_detected'):
            st.error(f"Drift Detected — Severity: {drift.get('drift_severity','unknown').upper()}", icon="🚨")
            for change in drift.get('changed_behaviors', []):
                st.write(f"— {change}")
            st.warning(f"Recommendation: {drift.get('recommendation','N/A')}", icon="⚙️")
        else:
            st.success("Stable Baseline — No behavioral degradation detected.", icon="✓")
            st.info(drift.get('recommendation','Continuous monitoring active.'), icon="ℹ️")

        # ── Raw JSON ───────────────────────────────────────────────────────────
        st.markdown("---")
        with st.expander("Raw Diagnostic Payload (JSON)"):
            st.json(output)

    except Exception as e:
        status_text.error(f"Runtime Exception: {str(e)}")
        st.exception(e)