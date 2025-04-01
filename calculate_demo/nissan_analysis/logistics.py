
def fill_logistics(df_logistic, final_summary):
    try:
        val_ib = df_logistic.loc[df_logistic["Unnamed: 2"] == "I/B Total:", "Unnamed: 3"].values[0]
    except IndexError:
        val_ib = None
    try:
        val_ob = df_logistic.loc[df_logistic["Unnamed: 2"] == "O/B Total", "Unnamed: 3"].values[0]
    except IndexError:
        val_ob = None

    if val_ib is not None:
        final_summary.loc[
            final_summary["Description"] == "I/B Logistics",
            ["CLA", "LWR", "MID", "UPR"]
        ] = float(val_ib)

    if val_ob is not None:
        final_summary.loc[
            final_summary["Description"] == "O/B Logistics",
            ["CLA", "LWR", "MID", "UPR"]
        ] = float(val_ob)

    try:
        start_idx = final_summary[final_summary["Description"] == "I/B Logistics"].index[0]
        end_idx = final_summary[final_summary["Category"] == "Total Logistics"].index[0]
        logistics_sum = final_summary.loc[start_idx:end_idx, ["CLA", "LWR", "MID", "UPR"]].sum()
        for col in ["CLA", "LWR", "MID", "UPR"]:
            final_summary.at[end_idx, col] = logistics_sum[col]
    except:
        pass
