import pandas as pd
import streamlit as st
from io import BytesIO

st.title("🧹 Clean Distress Data")

uploaded_file = st.file_uploader("Upload Flattened CSV", type="csv")

if uploaded_file is not None:
    # Load DataFrame
    df = pd.read_csv(uploaded_file)

    # Get first (non-numeric) column
    non_numeric_col = df.columns[0]
    numeric_cols = df.columns[1:]

    # Convert to numeric (force errors to NaN) and fill NaN with 0
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.fillna(0, inplace=True)

    st.success("✅ Data cleaned. Preview below:")
    st.dataframe(df)

    # Download cleaned CSV
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=csv_data,
        file_name="cleaned_distress_data.csv",
        mime="text/csv"
    )
