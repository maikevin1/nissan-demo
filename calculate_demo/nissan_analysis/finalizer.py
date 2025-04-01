import pandas as pd

def build_final_summary(df_pxp, df_scrap, summary_results, weighted_summary, unweighted_summary, final_summary_bop):
    final_summary = final_summary_bop.copy()

    # Step 1: Add VEH MFG
    veh_mfg = pd.DataFrame({
        "Category": ["VAR VEH MFG", "FXD VEH MFG", "VAR VEH MFG", "FXD VEH MFG", "FXD VEH MFG"],
        "VAR/FIX": ["VAR", "FIX", "VAR", "FIX", "FIX"],
        "VEH/ENG": ["VEH"] * 5,
        "TDC": ["MFG"] * 5,
        "Description": [
            "Direct Labor", "Indirect Labor", "Processing Cost - VAR", "Processing Cost - FIX", "Tax"
        ],
        "CLA": [0] * 5, "LWR": [0] * 5, "MID": [0] * 5, "UPR": [0] * 5
    })
    veh_mfg_total = veh_mfg[["CLA", "LWR", "MID", "UPR"]].sum()
    final_summary = pd.concat([final_summary, veh_mfg], ignore_index=True)
    final_summary = pd.concat([final_summary, pd.DataFrame({
        "Category": ["Total VEH MFG"],
        "VAR/FIX": ["Total"], "VEH/ENG": ["VEH"], "TDC": ["MFG"],
        "Description": ["Total Summary"],
        "CLA": [veh_mfg_total["CLA"]], "LWR": [veh_mfg_total["LWR"]],
        "MID": [veh_mfg_total["MID"]], "UPR": [veh_mfg_total["UPR"]]
    })], ignore_index=True)

    # Step 2: Add ENG MFG
    eng_mfg = veh_mfg.copy()
    eng_mfg["VEH/ENG"] = "ENG"
    eng_mfg["Category"] = ["VAR ENG MFG", "FXD ENG MFG", "VAR ENG MFG", "FXD ENG MFG", "FXD ENG MFG"]
    final_summary = pd.concat([final_summary, eng_mfg], ignore_index=True)
    final_summary = pd.concat([final_summary, pd.DataFrame({
        "Category": ["Total ENG MFG"],
        "VAR/FIX": ["Total"], "VEH/ENG": ["ENG"], "TDC": ["MFG"],
        "Description": ["Total Summary"],
        "CLA": [0], "LWR": [0], "MID": [0], "UPR": [0]
    })], ignore_index=True)

    # Step 3: Add DEPREC（VEH & ENG 各一份）
    deprec = pd.DataFrame({
        "Category": ["DEPREC"] * 5,
        "VAR/FIX": ["FIX"] * 5,
        "VEH/ENG": ["VEH"] * 5,
        "TDC": ["DEP"] * 5,
        "Description": ["Machinery", "Tools", "Specific Tool", "Vendortooling", "General (Building Furniture etc.)"],
        "CLA": [0] * 5, "LWR": [0] * 5, "MID": [0] * 5, "UPR": [0] * 5
    })
    final_summary = pd.concat([final_summary, deprec], ignore_index=True)
    final_summary = pd.concat([final_summary, pd.DataFrame({
        "Category": ["Total VEH Depreciation"],
        "VAR/FIX": ["Total"], "VEH/ENG": ["VEH"], "TDC": ["DEP"],
        "Description": ["Total Summary"],
        "CLA": [0], "LWR": [0], "MID": [0], "UPR": [0]
    })], ignore_index=True)

    deprec_eng = deprec.copy()
    deprec_eng["VEH/ENG"] = "ENG"
    final_summary = pd.concat([final_summary, deprec_eng], ignore_index=True)
    final_summary = pd.concat([final_summary, pd.DataFrame({
        "Category": ["Total ENG Depreciation"],
        "VAR/FIX": ["Total"], "VEH/ENG": ["ENG"], "TDC": ["DEP"],
        "Description": ["Total Summary"],
        "CLA": [0], "LWR": [0], "MID": [0], "UPR": [0]
    })], ignore_index=True)

    # Step 4: Add Transmission
    transmission = pd.DataFrame({
        "Category": ["VAR T/M"] * 5 + ["FXD T/M"] * 2,
        "VAR/FIX": ["VAR"] * 5 + ["FIX"] * 2,
        "VEH/ENG": ["T/M"] * 7,
        "TDC": ["BOP", "BOP", "BOP", "LOG", "MFG", "MFG", "DEP"],
        "Description": [
            "Local", "KD", "Raw Material", "Inbound Logistic", "Variable and Labor", "MFG Fixed", "Depreciation"
        ],
        "CLA": [0] * 7, "LWR": [0] * 7, "MID": [0] * 7, "UPR": [0] * 7
    })
    final_summary = pd.concat([final_summary, transmission], ignore_index=True)
    final_summary = pd.concat([final_summary, pd.DataFrame({
        "Category": ["Total Transmission"],
        "VAR/FIX": ["Total"], "VEH/ENG": ["T/M"], "TDC": ["Total"],
        "Description": ["Total Summary"],
        "CLA": [0], "LWR": [0], "MID": [0], "UPR": [0]
    })], ignore_index=True)

    # Step 5: Final Drive Other
    final_summary = pd.concat([final_summary, pd.DataFrame({
        "Category": ["VAR T/M"], "VAR/FIX": ["VAR"], "VEH/ENG": ["VEH/ENG"],
        "TDC": ["OTH"], "Description": ["Final Drive Non-BOP Costs"],
        "CLA": [0], "LWR": [0], "MID": [0], "UPR": [0]
    })], ignore_index=True)
    final_summary = pd.concat([final_summary, pd.DataFrame({
        "Category": ["Total Final Drive Other"], "VAR/FIX": ["Total"], "VEH/ENG": ["VEH/ENG"],
        "TDC": ["OTH"], "Description": ["Total Summary"],
        "CLA": [0], "LWR": [0], "MID": [0], "UPR": [0]
    })], ignore_index=True)

    # Step 6: Logistics
    logistics = pd.DataFrame({
        "Category": ["LOGs", "LOGs"],
        "VAR/FIX": ["VAR", "VAR"],
        "VEH/ENG": ["VEH/ENG", "VEH/ENG"],
        "TDC": ["LOG", "OTH"],
        "Description": ["I/B Logistics", "O/B Logistics"],
        "CLA": [0, 0], "LWR": [0, 0], "MID": [0, 0], "UPR": [0, 0]
    })
    final_summary = pd.concat([final_summary, logistics], ignore_index=True)
    final_summary = pd.concat([final_summary, pd.DataFrame({
        "Category": ["Total Logistics"], "VAR/FIX": ["Total"], "VEH/ENG": ["VEH/ENG"],
        "TDC": ["Total"], "Description": ["Total Summary"],
        "CLA": [0], "LWR": [0], "MID": [0], "UPR": [0]
    })], ignore_index=True)

    # Step 7: Other COGS
    other_cogs = pd.DataFrame({
        "Category": ["WARR", "GLOB", "GLOB", "VAR OTHER", "FXD OTHER"],
        "VAR/FIX": ["VAR", "FIX", "FIX", "VAR", "FIX"],
        "VEH/ENG": ["VEH/ENG"] * 5,
        "TDC": ["WTY", "GLB", "GLB", "OTH", "OTH"],
        "Description": [
            "Contractual Warranty", "Recall/Service campaign", "Maintenance of current vehicles",
            "Complenmentary costs + Other - Variable", "Others - Fixed"
        ],
        "CLA": [0] * 5, "LWR": [0] * 5, "MID": [0] * 5, "UPR": [0] * 5
    })
    final_summary = pd.concat([final_summary, other_cogs], ignore_index=True)
    final_summary = pd.concat([final_summary, pd.DataFrame({
        "Category": ["Total Other COGS"], "VAR/FIX": ["Total"], "VEH/ENG": ["VEH/ENG"],
        "TDC": ["Total"], "Description": ["Total Summary"],
        "CLA": [0], "LWR": [0], "MID": [0], "UPR": [0]
    })], ignore_index=True)

    # Step 8: R&D
    rd = pd.DataFrame({
        "Category": ["R&D", "R&D", "GLOB", "GLOB"],
        "VAR/FIX": ["FIX"] * 4,
        "VEH/ENG": ["VEH/ENG"] * 4,
        "TDC": ["R&D", "R&D", "GLB", "GLB"],
        "Description": ["Ramp-up cost(PIC)", "Direct D&D", "D&D Division cost", "Research Cost"],
        "CLA": [0] * 4, "LWR": [0] * 4, "MID": [0] * 4, "UPR": [0] * 4
    })
    final_summary = pd.concat([final_summary, rd], ignore_index=True)
    final_summary = pd.concat([final_summary, pd.DataFrame({
        "Category": ["Total R&D"], "VAR/FIX": ["Total"], "VEH/ENG": ["VEH/ENG"],
        "TDC": ["Total"], "Description": ["Total Summary"],
        "CLA": [0], "LWR": [0], "MID": [0], "UPR": [0]
    })], ignore_index=True)

    return final_summary
