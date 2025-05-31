import streamlit as st
import pandas as pd
import time

from scripts.flatten import flatten_and_clean
from visualizations.pcigraph import show_visualizations
from scripts.summary import prepare_summary_for_llm
from scripts.llm_engine import analyze_with_llm

# Page config with custom browser tab icon
st.set_page_config(
    page_title="RunwAI – Pavement AI Assistant",
    page_icon="logo/image.png",  # Use your custom logo
    layout="wide"
)

# Layout: Logo + Title left, Uploader right
col1, col2 = st.columns([4, 1])

with col1:
    st.image("logo/image.png", width=60)  # Top-left logo
    st.markdown("## RunwAI – Pavement Condition Analyzer")
    st.markdown("##### FAA-aligned AI assistant for airport pavement assessment and treatment planning.")

with col2:
    uploaded_file = st.file_uploader("📤 Upload XLSX/XLSM", type=["xlsx", "xlsm"])

# Status + PCI (fill header gap)
with col1:
    if uploaded_file:
        try:
            df_cleaned = flatten_and_clean(uploaded_file)
            avg_pci = df_cleaned['PCI Score'].mean()

            st.markdown("✅ File processed successfully!")
            st.markdown(
                f"""
                <div style="padding: 0.5rem 1rem; background-color: #E9F5FF; border-radius: 10px; width: fit-content; margin-top: 0.5rem;">
                    <b>📊 Average PCI:</b> <span style="font-size: 1.4rem; color: #0072CE;"><b>{avg_pci:.1f}</b></span>
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
    else:
        st.info("📎 Please upload a file to get started.")

# Main content (only run if file is processed)
if uploaded_file:
    try:
        if "df_cleaned" not in locals():
            df_cleaned = flatten_and_clean(uploaded_file)

        # Tabs for visual analysis and AI
        tab1, tab2 = st.tabs(["📈 Visual Insights", "🧠 AI Recommendations"])

        with tab1:
            show_visualizations(df_cleaned)

        with tab2:
            summary_text = prepare_summary_for_llm(df_cleaned)
            st.markdown("Click the button below to get AI-powered pavement treatment recommendations.")

            if st.button("🔍 Want AI-based suggestions? Analyze"):
                with st.spinner("🤖 Talking to the AI Engineer..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    ai_response = analyze_with_llm(summary_text)

                st.success("🧠 AI Analysis Complete!")
                with st.expander("📋 Full Recommendation", expanded=True):
                    st.markdown(ai_response.replace("\n", "  \n"))

    except Exception as e:
        st.error(f"❌ Error analyzing file: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    "<center><sub>Powered by RunwAI • FAA Pavement AI Tools • v1.0</sub></center>",
    unsafe_allow_html=True
)
