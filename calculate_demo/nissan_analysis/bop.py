import pandas as pd
import numpy as np

def process_bop(df_bop):
    # Step A: Build summary_results
    cost_groups = df_bop["COST GROUP"].unique()
    trim_categories = df_bop["TRIM"].unique()
    summary_results = pd.DataFrame(columns=["COST GROUP"] + list(trim_categories))

    for cost in cost_groups:
        row = [cost]
        for trim in trim_categories:
            val = df_bop.loc[(df_bop["COST GROUP"]==cost) & (df_bop["TRIM"]==trim), "TOTAL_COST"].sum()
            row.append(val)
        summary_results.loc[len(summary_results)] = row

    # Step B: label mapping
    label_map = {
        "Local BOP": ["POWERTRAIN LOCAL", "VEHICLE LOCAL"],
        "MAT":       ["BULK-ENG LOCAL", "BULK-VEH LOCAL", "STEEL-VEH LOCAL"],
        "KD":        ["ENGINE KD", "POWERTRAIN KD"],
        "ENG":       ["ENGINE LOCAL"],
        "PGM":       ["PGM LOCAL"],
        "VAR T/M":   ["TRANSMISSION KD", "TRANSMISSION LOCAL"]
    }
    def assign_label(g):
        for lbl, arr in label_map.items():
            if g in arr:
                return lbl
        return "Other"

    summary_results["Label"] = summary_results["COST GROUP"].apply(assign_label)

    # Step C: unweighted_summary (to fill LWR/MID/UPR)
    unweighted_summary = summary_results.groupby("Label").sum(numeric_only=True).reset_index()

    # Step D: Weighted (CLA)
    df_melt = summary_results.melt(id_vars=["COST GROUP","Label"], var_name="TRIM", value_name="TOTAL_COST")
    mix_df = df_bop[["TRIM","MIX"]].drop_duplicates().reset_index(drop=True)
    df_melt = df_melt.merge(mix_df, on="TRIM", how="left")
    df_melt["Weighted"] = df_melt["TOTAL_COST"] * df_melt["MIX"]
    cla_df = df_melt.groupby("Label")["Weighted"].sum().reset_index().rename(columns={"Weighted":"CLA"})

    # Step E: final_summary
    template = [
        {"Category":"ENG",        "Description":"Powertrain cost analysis"},
        {"Category":"KD",         "Description":"Bulk material cost"},
        {"Category":"Local BOP",  "Description":"Engine cost distribution"},
        {"Category":"MAT",        "Description":"Fixed engine costs"},
        {"Category":"Other",      "Description":"Program cost allocation"},
        {"Category":"PGM",        "Description":"Transmission cost variance"},
        {"Category":"VAR T/M",    "Description":"Vehicle cost breakdown"},
        {"Category":"MAT",        "Description":"Centralized Steel"},
        {"Category":"MAT",        "Description":"In-House Scrap Recycling"},
        {"Category":"Total BOP",  "Description":"Total Summary"}
    ]
    final_summary = pd.DataFrame(template)
    final_summary["VAR/FIX"] = "VAR"
    final_summary["TDC"] = "BOP"

    veh_eng_map = {"ENG":"ENG","Local BOP":"VEH","MAT":"VEH","PGM":"ENG","KD":"VEH"}
    final_summary["VEH/ENG"] = final_summary["Category"].apply(lambda x: veh_eng_map.get(x,"Total"))

    final_summary["CLA"]=0.0
    final_summary["LWR"]=0.0
    final_summary["MID"]=0.0
    final_summary["UPR"]=0.0

    # Fill CLA from cla_df
    for i, row in final_summary.iterrows():
        cat = row["Category"]
        match = cla_df.loc[cla_df["Label"]==cat]
        if not match.empty:
            final_summary.at[i,"CLA"] = match["CLA"].values[0]

    # Fill LWR/MID/UPR from unweighted_summary
    for i, row in final_summary.iterrows():
        cat = row["Category"]
        match = unweighted_summary.loc[unweighted_summary["Label"]==cat]
        if not match.empty:
            arr = match.iloc[:,1:].values.flatten()  # skip "Label" col
            final_summary.at[i,"LWR"] = arr.min()
            final_summary.at[i,"MID"] = np.median(arr)
            final_summary.at[i,"UPR"] = arr.max()

    # Step F: compute "Total BOP"
    # sum up all rows except "Total BOP"
    bop_idx = final_summary[final_summary["Category"]=="Total BOP"].index[0]
    sub_bop = final_summary.loc[final_summary.index!=bop_idx, ["CLA","LWR","MID","UPR"]].sum()
    final_summary.loc[bop_idx, ["CLA","LWR","MID","UPR"]] = sub_bop.values

    # Return 4 results
    return summary_results, cla_df, unweighted_summary, final_summary