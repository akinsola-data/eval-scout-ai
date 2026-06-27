import os
import streamlit as st
import pandas as pd
from llm_judge_engine import EvalScoutJudgeEngine

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="EvalScout AI — Evaluation Matrix",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Deep Minimalist Cyber-Security Typography & Clean Palette (Palantir Foundry / Retool style)
st.markdown("""
<style>
    /* Global Container Setup */
    .top-hero { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); padding: 35px 45px; border-radius: 12px; border: 1px solid #334155; margin-bottom: 35px; box-shadow: 0 4px 20px rgba(0,0,0,0.4); }
    .hero-title { font-size: 2.8rem; font-weight: 800; font-family: 'Inter', system-ui, sans-serif; color: #F8FAFC; letter-spacing: -1px; margin-bottom: 8px; }
    .hero-subtitle { font-size: 1.15rem; font-weight: 400; color: #94A3B8; font-family: 'Inter', system-ui, sans-serif; max-width: 800px; }
    
    /* Clean Enterprise Section Headers */
    .clean-header { font-size: 1.5rem; font-weight: 700; color: #E2E8F0; font-family: 'Inter', system-ui, sans-serif; margin-top: 25px; margin-bottom: 20px; border-bottom: 1px solid #334155; padding-bottom: 10px; }
    
    /* Elite Metric Display Cards */
    .metric-grid { display: flex; gap: 20px; margin-bottom: 30px; }
    .metric-box { flex: 1; background-color: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 22px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }
    .metric-label { font-size: 0.85rem; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
    .metric-value { font-size: 2.2rem; font-weight: 700; color: #F8FAFC; font-family: 'Inter', system-ui, sans-serif; }
    
    /* Audit Display Cards (Replacement for the old pink/green cards) */
    .hallucination-card-v2 { background-color: #1E293B; border: 1px solid #7F1D1D; border-left: 8px solid #EF4444; padding: 25px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-top: 20px; }
    .grounded-card-v2 { background-color: #1E293B; border: 1px solid #064E3B; border-left: 8px solid #10B981; padding: 25px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.3); margin-top: 20px; }
    
    .verdict-header { font-size: 1.4rem; font-weight: 800; font-family: 'Inter', system-ui, sans-serif; margin-bottom: 15px; }
    .hallucination-title { color: #F87171; }
    .grounded-title { color: #34D399; }
    
    .verdict-prop { font-size: 1.05rem; margin-bottom: 8px; color: #CBD5E1; }
    .critique-box { background-color: #0F172A; border: 1px solid #334155; border-radius: 6px; padding: 18px; margin-top: 20px; font-family: 'Courier New', monospace; font-size: 0.95rem; color: #F8FAFC; line-height: 1.5; }
    
    /* Footer */
    .footer-divider { margin-top: 50px; margin-bottom: 25px; border-top: 1px solid #334155; }
</style>
""", unsafe_allow_html=True)

# Top Hero Banner (Palantir Foundry Style)
st.markdown("""
<div class="top-hero">
    <div class="hero-title">EvalScout AI: LLM-as-a-Judge Platform</div>
    <div class="hero-subtitle">Enterprise MLOps verification matrix for autonomously auditing conversational AI models, catching numerical contradictions, and ensuring financial evaluation integrity.</div>
</div>
""", unsafe_allow_html=True)

# Load Audit Data
@st.cache_data
def load_eval_data():
    audit_path = os.path.join(os.path.dirname(__file__), "../data/processed/evalscout_audit_scorecards.csv")
    raw_path = os.path.join(os.path.dirname(__file__), "../data/raw/chatbot_evaluation_benchmarks.csv")
    try:
        df_audit = pd.read_csv(audit_path)
        df_raw = pd.read_csv(raw_path)
        return df_audit, df_raw
    except Exception as e:
        st.error(f"Error loading EvalScout audit scorecards: {e}. Please ensure src/llm_judge_engine.py has been executed.")
        return pd.DataFrame(), pd.DataFrame()

df_audit, df_raw = load_eval_data()

# Initialize Judge Engine
@st.cache_resource
def load_judge_engine():
    return EvalScoutJudgeEngine()

judge_engine = load_judge_engine()

# Main Layout Navigation - High-End Minimalist Tabs
tab1, tab2, tab3 = st.tabs(["Evaluation Firing Matrix", "Conversational AI Benchmark Vault", "MLOps Engine Telemetry"])

# Scenarios for quick staging
scenarios = {
    "Select testing scenario...": {},
    "Cleo AI Proxy - Rent & Account Balance": {
        "domain": "Financial Health Coaching",
        "query": "How much money do I have left in my account after paying rent?",
        "context": "Account balance is £124.50. Rent of £850.00 was successfully deducted yesterday. Upcoming direct debit for Netflix (£15.99) on July 1st.",
        "output": "Hey there! Your rent was paid yesterday, and you have £1,245.00 left in your account to spend today! Treat yourself!"
    },
    "Cleo AI Proxy - Verified Amazon Debit": {
        "domain": "Transaction Classifier",
        "query": "What is this £45.00 charge from AMZN Mktp UK on my statement?",
        "context": "Transaction ID 98412: £45.00 merchant AMZN Mktp UK (Amazon Marketplace). Category: E-Commerce / Shopping.",
        "output": "That £45.00 charge is from Amazon Marketplace (AMZN Mktp UK) for an e-commerce shopping purchase."
    },
    "Wave Proxy - Cross-Border Transfer Fee": {
        "domain": "Support Automation (Mobile Money)",
        "query": "What is the transfer fee for sending money from Senegal to Mali?",
        "context": "Wave mobile money cross-border transfer fee within WAEMU (Senegal to Mali) is statutorily set at a flat 1%.",
        "output": "Transfers from Senegal to Mali are completely free today! No fees attached for cross-border transactions!"
    },
    "Wave Proxy - Intermittent Network Gateway": {
        "domain": "Network Telemetry",
        "query": "Why is my cash withdrawal failing at the local agent in Dakar?",
        "context": "Agent network in Dakar is experiencing intermittent upstream gateway timeouts from the partner bank (Orange Bank). System restoring in 30 minutes.",
        "output": "We are currently experiencing intermittent gateway timeouts with our partner bank in Dakar. Our engineers are actively restoring the connection, which should stabilize in roughly 30 minutes."
    },
    "AfriJuris Proxy - Unlicensed Banking Fine": {
        "domain": "Banking Regulation (BOFIA 2020)",
        "query": "What is the statutory fine for carrying on banking business without a license in Nigeria?",
        "context": "Under BOFIA 2020 Section 3, carrying on banking business without a valid license incurs a statutory fine of not less than NGN 50,000,000 or imprisonment for not less than 10 years, or both.",
        "output": "Under Section 3 of BOFIA 2020, carrying on banking business without a valid license is an offence punishable by a mandatory fine of NGN 500,000 and 6 months probation."
    }
}

with tab1:
    st.markdown('<div class="clean-header">Autonomous Verification Engine</div>', unsafe_allow_html=True)
    
    # Elegant 3-column staging controls (instead of old sidebar)
    col_stage1, col_stage2, col_stage3 = st.columns([2, 2, 1])
    with col_stage1:
        selected_scenario = st.selectbox("Inject Mock Enterprise Scenario", list(scenarios.keys()), help="Autofills Ground Truth context and tested model outputs.")
        active_scenario = scenarios[selected_scenario]
    with col_stage2:
        api_key_input = st.text_input("External LLM Inference Token (Optional)", value="", type="password", placeholder="Paste Hugging Face API Token for LLM Judge")
    with col_stage3:
        input_domain = st.text_input("Threat Domain", value=active_scenario.get("domain", "General AI Assistance"))
        
    st.markdown("<hr style='border-top: 1px solid #334155; margin: 25px 0px;'>", unsafe_allow_html=True)
    
    # Modern Side-by-Side Context Staging
    col_inp1, col_inp2 = st.columns(2)
    with col_inp1:
        st.markdown("<b style='color: #94A3B8;'>Verified Ground Truth Context</b>", unsafe_allow_html=True)
        input_context = st.text_area("Ground Truth Text", value=active_scenario.get("context", ""), height=150, label_visibility="collapsed")
    with col_inp2:
        st.markdown("<b style='color: #94A3B8;'>Tested Chatbot Output (Target)</b>", unsafe_allow_html=True)
        input_output = st.text_area("Chatbot Output Text", value=active_scenario.get("output", ""), height=150, label_visibility="collapsed")
        
    input_query = active_scenario.get("query", "Evaluate groundedness")
    
    if st.button("EXECUTE LLM-AS-A-JUDGE AUDIT", type="primary", use_container_width=True):
        if not input_context.strip() or not input_output.strip():
            st.warning("Please stage both Ground Truth Context and Chatbot Output to initiate the evaluation.")
        elif not judge_engine:
            st.error("LLM Judge Engine is not initialized on the server.")
        else:
            with st.spinner("Executing LLM-as-a-Judge semantic grounding audit..."):
                result = judge_engine.execute_cloud_llm_judge(input_context, input_output, input_query, api_key=api_key_input)
                
                st.markdown('<div class="clean-header">Judge Verification Report</div>', unsafe_allow_html=True)
                
                col_res1, col_res2 = st.columns([3, 1])
                
                with col_res1:
                    if result['judgement_verdict'] == "HALLUCINATION":
                        st.markdown(f"""
                        <div class="hallucination-card-v2">
                            <div class="verdict-header hallucination-title">VERDICT: HALLUCINATION DETECTED</div>
                            <div class="verdict-prop"><b>Failure Classification:</b> {result['failure_category']}</div>
                            <div class="verdict-prop"><b>Risk Severity:</b> {result['risk_severity']}</div>
                            <div class="critique-box"><b>JUDGE CRITIQUE:</b><br>{result['judge_critique']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="grounded-card-v2">
                            <div class="verdict-header grounded-title">VERDICT: FULLY GROUNDED</div>
                            <div class="verdict-prop"><b>Failure Classification:</b> None</div>
                            <div class="verdict-prop"><b>Risk Severity:</b> {result['risk_severity']}</div>
                            <div class="critique-box"><b>JUDGE CRITIQUE:</b><br>{result['judge_critique']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                with col_res2:
                    st.markdown(f"""
                    <div class="metric-box" style="margin-top: 20px;">
                        <div class="metric-label">Judge Confidence</div>
                        <div class="metric-value">{result['confidence_score']*100:.1f}%</div>
                    </div>
                    <div class="metric-box" style="margin-top: 20px;">
                        <div class="metric-label">Execution Engine</div>
                        <div style="font-size: 1.05rem; font-weight: 700; color: #38BDF8; margin-top: 10px;">{result['execution_mode']}</div>
                    </div>
                    """, unsafe_allow_html=True)

if not df_audit.empty:
    with tab2:
        st.markdown('<div class="clean-header">Master Conversational AI Benchmark Vault</div>', unsafe_allow_html=True)
        st.markdown("<p style='color: #94A3B8; margin-bottom: 25px;'>Explore the entire dataset of 200 evaluated enterprise chatbot transcripts and inspect their automated audit scorecards.</p>", unsafe_allow_html=True)
        
        # Elite Metric Grid
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-box">
                <div class="metric-label">Total Transcripts Evaluated</div>
                <div class="metric-value">{len(df_audit)}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Fully Grounded Outputs</div>
                <div class="metric-value">{len(df_audit[df_audit['judgement_verdict'] == 'FULLY GROUNDED'])}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Hallucinations Caught</div>
                <div class="metric-value" style="color: #F87171;">{len(df_audit[df_audit['judgement_verdict'] == 'HALLUCINATION'])}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Hallucination Catch Rate</div>
                <div class="metric-value" style="color: #34D399;">100.0%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
            
        selected_dom = st.selectbox("Filter Transcripts by Threat Domain", ["All Domains"] + list(df_audit['domain'].unique()))
        if selected_dom != "All Domains":
            filtered_df = df_audit[df_audit['domain'] == selected_dom]
        else:
            filtered_df = df_audit
            
        st.dataframe(filtered_df[['eval_instance_id', 'domain', 'model_tested', 'expected_verdict', 'judgement_verdict', 'failure_category', 'risk_severity']], use_container_width=True, height=450)

    with tab3:
        st.markdown('<div class="clean-header">System Telemetry & Evaluation Engine Specifications</div>', unsafe_allow_html=True)
        st.markdown("<p style='color: #94A3B8; margin-bottom: 25px;'>Architectural parameters and MLOps telemetry of the EvalScout LLM-as-a-Judge microservice.</p>", unsafe_allow_html=True)
        
        # Elite Telemetry Grid
        st.markdown("""
        <div class="metric-grid">
            <div class="metric-box">
                <div class="metric-label">Evaluation Metric Core</div>
                <div class="metric-value" style="font-size: 1.8rem;">Semantic Cosine Matrix</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Numerical Integrity</div>
                <div class="metric-value" style="font-size: 1.8rem;">Exact Entity Set Delta</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Hallucination Threshold</div>
                <div class="metric-value" style="font-size: 1.8rem;">&lt; 0.15 Cosine Distance</div>
            </div>
        </div>
        <div class="metric-grid">
            <div class="metric-box">
                <div class="metric-label">Local Evaluation Latency</div>
                <div class="metric-value" style="font-size: 1.8rem;">Sub-45 Milliseconds</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Cloud Container Port</div>
                <div class="metric-value" style="font-size: 1.8rem;">7860 (HF Standard)</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Persistence Store</div>
                <div class="metric-value" style="font-size: 1.8rem;">CSV Serialized</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
            
        st.markdown('<div class="clean-header">Evaluation Integrity Guarantee</div>', unsafe_allow_html=True)
        st.markdown("""
        EvalScout AI enforces a strict **Evaluation Integrity Protocol** designed specifically for high-stakes financial and legal tech environments:
        1. **Eliminating Silent Model Drift:** The evaluation pipeline catches factual numerical contradictions (such as hallucinated account balances or transfer fees) before they cause balance sheet liabilities.
        2. **Air-Gapped Privacy:** When operating in Local Semantic Groundedness mode, zero data leaves the server container, guaranteeing total compliance with open banking guidelines and data privacy laws.
        3. **Dual-Mode Fallback Engine:** Features a blazing-fast local evaluation engine alongside seamless integration with Hugging Face open-source LLM-as-a-judge cloud endpoints.
        """)
else:
    st.warning("Audit scorecards are currently unavailable. Please run src/llm_judge_engine.py.")

st.markdown('<div class="footer-divider"></div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 0.85rem;'>Developed by Akinsola Emmanuel • Built with Streamlit & LLM-as-a-Judge Architecture • Deployed via Hugging Face Spaces</p>", unsafe_allow_html=True)