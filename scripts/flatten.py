import pandas as pd

def extract_pci_from_sheet(df):
    for i in range(len(df)):
        for j in range(len(df.columns)):
            cell = df.iat[i, j]
            if isinstance(cell, str) and "pci (100-max cdv)" in cell.lower():
                for offset in range(1, 10):
                    if j + offset < len(df.columns):
                        candidate = df.iat[i, j + offset]
                        try:
                            if pd.notna(candidate):
                                val = float(candidate)
                                if val <= 100:
                                    return int(val)
                        except:
                            continue
    return None

def find_header_row(df):
    expected_headers = ["distress & severity", "total", "density %", "deduct value"]
    for i in range(min(30, len(df))):
        row = df.iloc[i].astype(str).str.lower().str.strip().fillna("")
        if all(h in row.values for h in expected_headers):
            return i, {
                "distress": row[row == "distress & severity"].index[0],
                "total": row[row == "total"].index[0],
                "density": row[row == "density %"].index[0],
                "deduct": row[row == "deduct value"].index[0],
            }
    return None, {}

def safe_number(value):
    try:
        return float(value)
    except:
        return 0

def flatten_and_clean(file):
    ext = file.name.split(".")[-1].lower()
    engine = "openpyxl" if ext in ["xlsm", "xlsx"] else None

    xls = pd.ExcelFile(file, engine=engine)
    all_distresses = set()
    flattened_rows = []
    temp_storage = []

    for sheet in xls.sheet_names:
        if not sheet.lower().startswith("sample unit"):
            continue
        df = pd.read_excel(xls, sheet_name=sheet, engine=engine, header=None)
        pci_score = extract_pci_from_sheet(df)
        flat_row = {"Sheet Name": sheet, "PCI Score": pci_score}
        header_row, col_map = find_header_row(df)
        if not col_map:
            continue

        last_distress = None
        data_block = []

        for i in range(header_row + 1, len(df)):
            row = df.iloc[i]
            distress = row[col_map["distress"]] if col_map["distress"] in row.index else None
            total = safe_number(row[col_map["total"]])
            density = safe_number(row[col_map["density"]])
            deduct = safe_number(row[col_map["deduct"]])

            if pd.isna(distress) and total == 0 and density == 0 and deduct == 0:
                break

            if pd.notna(distress):
                distress = str(distress).strip()
                if not any(c.isalpha() for c in distress):  # 🛡️ skip invalid numeric-like names
                    continue
                last_distress = distress
            elif last_distress:
                distress = last_distress
            else:
                continue

            name = str(distress).strip()
            data_block.append([name, total, density, deduct])
            all_distresses.add(name)

        present = set()
        for name, total, density, deduct in data_block:
            present.add(name)
            flat_row[f"{name} - Total"] = total
            flat_row[f"{name} - Density %"] = density
            flat_row[f"{name} - Deduct Value"] = deduct

        temp_storage.append((flat_row, present))

    for row, present in temp_storage:
        for distress in all_distresses:
            if distress not in present:
                row[f"{distress} - Total"] = 0
                row[f"{distress} - Density %"] = 0
                row[f"{distress} - Deduct Value"] = 0
        flattened_rows.append(row)

    df_final = pd.DataFrame(flattened_rows)

    # Clean numeric columns except the first
    for col in df_final.columns[1:]:
        df_final[col] = pd.to_numeric(df_final[col], errors='coerce')
    df_final.fillna(0, inplace=True)

    return df_final
