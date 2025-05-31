import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def show_visualizations(df: pd.DataFrame):
    df.columns = df.columns.str.strip()
    df.fillna(0, inplace=True)

    if "PCI Score" not in df.columns:
        st.warning("❌ 'PCI Score' column not found.")
        return

    avg_pci = df["PCI Score"].mean().round(2)
    st.metric(label="Average PCI Score", value=avg_pci)

    deduct_cols = [col for col in df.columns if "Deduct Value" in col and col != "PCI Score"]

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("### PCI Distribution")
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        sns.histplot(df["PCI Score"], bins=10, kde=False, color='skyblue', ax=ax1)
        ax1.set_title("PCI Score Histogram", fontsize=12)
        ax1.set_xlabel("PCI Range", fontsize=10)
        ax1.set_ylabel("Count", fontsize=10)
        ax1.tick_params(labelsize=8)
        st.pyplot(fig1)

    with col2:
        view_option = st.radio("Choose view:", ["Top 15 Total Impact", "Top 15 Avg Impact"], horizontal=True)

        if view_option == "Top 15 Total Impact":
            total_impact = df[deduct_cols].sum().sort_values(ascending=False).head(15)
            fig2, ax2 = plt.subplots(figsize=(7, 5))
            sns.barplot(x=total_impact.values, y=total_impact.index, palette="viridis", ax=ax2)
            ax2.set_title("Top 15 Total Deduct Values", fontsize=12)
            ax2.set_xlabel("Sum", fontsize=10)
            ax2.set_ylabel("Distress", fontsize=10)
            ax2.tick_params(labelsize=8)
            st.pyplot(fig2)
        else:
            avg_impact = df[deduct_cols].mean().sort_values(ascending=False).head(15)
            fig3, ax3 = plt.subplots(figsize=(7, 5))
            sns.barplot(x=avg_impact.values, y=avg_impact.index, palette="magma", ax=ax3)
            ax3.set_title("Top 15 Average Deduct Values", fontsize=12)
            ax3.set_xlabel("Average", fontsize=10)
            ax3.set_ylabel("Distress", fontsize=10)
            ax3.tick_params(labelsize=8)
            st.pyplot(fig3)
