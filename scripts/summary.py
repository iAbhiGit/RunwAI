import pandas as pd

def prepare_summary_for_llm(df: pd.DataFrame) -> str:
    df.columns = df.columns.str.strip()
    df.fillna(0, inplace=True)

    if "PCI Score" not in df.columns:
        return "PCI Score column not found."

    summary_lines = []

    # Basic PCI stats
    avg_pci = round(df["PCI Score"].mean(), 2)
    min_pci = round(df["PCI Score"].min(), 2)
    max_pci = round(df["PCI Score"].max(), 2)
    below_60_count = (df["PCI Score"] < 60).sum()

    summary_lines.append(f"Average PCI Score: {avg_pci}")
    summary_lines.append(f"Minimum PCI Score: {min_pci}")
    summary_lines.append(f"Maximum PCI Score: {max_pci}")
    summary_lines.append(f"Number of segments with PCI < 60: {below_60_count}")

    # PCI Distribution
    pci_bins = [0, 10, 25, 40, 55, 70, 85, 100]
    pci_labels = ["Failed", "Serious", "Very Poor", "Poor", "Fair", "Satisfactory", "Good"]
    pci_distribution = pd.cut(df["PCI Score"], bins=pci_bins, labels=pci_labels, include_lowest=True)
    pci_counts = pci_distribution.value_counts().sort_index()
    summary_lines.append("\nPCI Score Distribution:")
    for label, count in pci_counts.items():
        summary_lines.append(f"  - {label}: {count} segments")

    # Distress deduct value columns
    deduct_cols = [col for col in df.columns if "Deduct Value" in col and col != "PCI Score"]

    # Top 15 Total Deduct
    total_impact = df[deduct_cols].sum().sort_values(ascending=False).head(15)
    summary_lines.append("\nTop 15 Distresses by Total Deduct Value:")
    for name, val in total_impact.items():
        summary_lines.append(f"  - {name}: {val:.2f}")

    # Top 15 Avg Deduct
    avg_impact = df[deduct_cols].mean().sort_values(ascending=False).head(15)
    summary_lines.append("\nTop 15 Distresses by Average Deduct Value:")
    for name, val in avg_impact.items():
        summary_lines.append(f"  - {name}: {val:.2f}")

    # Bottom 5 PCI segments
    if "Sample Unit" in df.columns:
        worst = df[["Sample Unit", "PCI Score"]].sort_values(by="PCI Score").head(5)
        summary_lines.append("\nBottom 5 Segments by PCI Score:")
        for _, row in worst.iterrows():
            summary_lines.append(f"  - Sample {row['Sample Unit']}: PCI {row['PCI Score']}")

    return "\n".join(summary_lines)
