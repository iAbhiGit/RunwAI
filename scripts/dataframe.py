import pandas as pd

# 📄 File path to your dataset
file_path = "/Users/abhijeetbhalekar/Documents/pavesheet2csv/merged_final_distress_data_with_pci.csv"

# 🆕 Load into a new DataFrame called `distress_df`
distress_df = pd.read_csv(file_path)

# 🧹 Basic cleaning
distress_df.columns = distress_df.columns.str.strip()  # remove extra spaces from column names
distress_df.dropna(axis=1, how='all', inplace=True)    # drop fully empty columns
distress_df.dropna(axis=0, how='all', inplace=True)    # drop fully empty rows

# 💡 Optional: fill missing values with 0 (depends on your use case)
# distress_df.fillna(0, inplace=True)

# ✅ Show first few rows
print(distress_df.head())

# ✅ Show column names
print("\n🧾 Columns in the file:")
print(distress_df.columns.tolist())
