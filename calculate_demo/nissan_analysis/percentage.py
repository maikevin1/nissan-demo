import pandas as pd

def compute_percent_by_category(final_summary: pd.DataFrame) -> pd.DataFrame:
    filtered = final_summary[
        ~final_summary["Description"].str.contains("Total Summary|Grand Total", case=False, na=False) &
        ~final_summary["Category"].str.contains("Total", case=False, na=False)
    ].copy()

 
    cols = ["VAR/FIX", "Category", "CLA", "LWR", "MID", "UPR"]
    df = filtered[cols].copy()

    grouped = df.groupby(["VAR/FIX", "Category"]).sum(numeric_only=True).reset_index()

    total_cla = grouped["CLA"].sum()
    total_lwr = grouped["LWR"].sum()
    total_mid = grouped["MID"].sum()
    total_upr = grouped["UPR"].sum()

    grouped["CLA (%)"] = grouped["CLA"] / total_cla * 100
    grouped["LWR (%)"] = grouped["LWR"] / total_lwr * 100
    grouped["MID (%)"] = grouped["MID"] / total_mid * 100
    grouped["UPR (%)"] = grouped["UPR"] / total_upr * 100

    result = grouped[["VAR/FIX", "Category", "CLA (%)", "LWR (%)", "MID (%)", "UPR (%)"]]

    return result
