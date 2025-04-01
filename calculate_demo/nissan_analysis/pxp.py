
import numpy as np

def fill_pxp_values(df_pxp, final_summary):
    df_pxp["Unnamed: 1"] = df_pxp["Unnamed: 1"].astype(str).str.strip()

    desc_to_keywords = {
        "Direct Labor": ["Direct Labor Total"],
        "Indirect Labor": ["Indirect Labor Total"],
        "Processing Cost - VAR": ["Processing Cost Variable Production Direct"],
        "Processing Cost - FIX": [
            "Processing Cost Fixed Production Direct",
            "Processing Cost Fixed Mfg. Common"
        ],
        "Tax": ["Tax Total"]
    }

    desc_deprec = {
        "Machinery": ["Depreciation - Machinery"],
        "Tools": ["Depreciation - Tools"],
        "Specific Tool": ["Depreciation - Specific Tool"],
        "Vendortooling": ["Depreciation - Vendortooling"],
        "General (Building Furniture etc.)": ["Depreciation - General (Building Furniture etc.)"]
    }

    def fill_block(desc_map, column, veh_eng, total_label):
        for desc, keywords in desc_map.items():
            matched = df_pxp[df_pxp["Unnamed: 1"].isin(keywords)]
            if matched.empty:
                continue
            values = matched[column].astype(str).str.replace(",", "").str.strip()
            values = values.replace(["", "-", "NaN", "nan"], np.nan).dropna().astype(float)
            total_value = values.sum()
            mask = (final_summary["Description"] == desc) & (final_summary["VEH/ENG"] == veh_eng)
            final_summary.loc[mask, ["CLA", "LWR", "MID", "UPR"]] = total_value

        try:
            start = final_summary[
                (final_summary["Description"] == list(desc_map.keys())[0]) & 
                (final_summary["VEH/ENG"] == veh_eng)
            ].index[0]
            end = final_summary[final_summary["Category"] == total_label].index[0]
            block_sum = final_summary.loc[start:end, ["CLA", "LWR", "MID", "UPR"]].sum()
            for col in ["CLA", "LWR", "MID", "UPR"]:
                final_summary.at[end, col] = block_sum[col]
        except:
            pass

    fill_block(desc_to_keywords, "Unnamed: 44", "VEH", "Total VEH MFG")
    fill_block(desc_to_keywords, "Unnamed: 84", "ENG", "Total ENG MFG")
    fill_block(desc_deprec, "Unnamed: 44", "VEH", "Total VEH Depreciation")
    fill_block(desc_deprec, "Unnamed: 84", "ENG", "Total ENG Depreciation")
