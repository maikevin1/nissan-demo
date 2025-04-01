import pandas as pd
import numpy as np

def fill_from_pqcop_block(df_pqcop, final_summary, mapping, total_label, start_marker_col, start_marker_val, source_col, keyword_col):
    df_pqcop[keyword_col] = df_pqcop[keyword_col].astype(str).str.strip()
    df_pqcop[start_marker_col] = df_pqcop[start_marker_col].astype(str).str.strip()
    try:
        start_idx = df_pqcop[df_pqcop[start_marker_col] == start_marker_val].index[0] + 1
    except IndexError:
        return

    for desc, keywords in mapping.items():
        keywords = [kw.strip() for kw in keywords]
        match_section = df_pqcop.loc[start_idx:, keyword_col]
        matched_rows = match_section[match_section.isin(keywords)].index

        if not matched_rows.empty:
            try:
                values = (
                    df_pqcop.loc[matched_rows, source_col]
                    .astype(str)
                    .str.replace(",", "")
                    .replace(" ", np.nan)
                    .dropna()
                    .astype(float)
                )
                total_value = values.sum()
            except:
                total_value = 0

            final_summary.loc[
                final_summary["Description"] == desc,
                ["CLA", "LWR", "MID", "UPR"]
            ] = total_value

    try:
        first_desc = list(mapping.keys())[0]
        start_idx = final_summary[final_summary["Description"] == first_desc].index[0]
        end_idx = final_summary[final_summary["Category"] == total_label].index[0]
        block_sum = final_summary.loc[start_idx:end_idx, ["CLA", "LWR", "MID", "UPR"]].sum()
        for col in ["CLA", "LWR", "MID", "UPR"]:
            final_summary.at[end_idx, col] = block_sum[col]
    except:
        pass

def fill_pqcop_values(df_pqcop, final_summary):
    desc_to_keywords_other_cogs = {
        "Contractual Warranty": ["Contractual Warranty"],
        "Recall/Service campaign": ["Recall/Service Campaign", "Recall & Service Campaign"],
        "Maintenance of current vehicles": ["Maintenance Of Existing Models"],
        "Complenmentary costs + Other - Variable": ["Complementary Costs", "Others Variable"],
        "Others - Fixed": ["Others Fixed"]
    }
    desc_to_keywords_rd = {
        "Ramp-up cost(PIC)": ["Pre Act Cost"],
        "Direct D&D": ["Direct D&D Cost"],
        "D&D Division cost": ["D&D Division Cost"],
        "Research Cost": ["Research Cost"]
    }

    fill_from_pqcop_block(
        df_pqcop, final_summary,
        mapping=desc_to_keywords_other_cogs,
        total_label="Total Other COGS",
        start_marker_col="2023 Q3 ACT YTD FINAL",
        start_marker_val="2023 Q4 ACT YTD FLASH",
        source_col="Unnamed: 4",
        keyword_col="Unnamed: 0"
    )

    fill_from_pqcop_block(
        df_pqcop, final_summary,
        mapping=desc_to_keywords_rd,
        total_label="Total R&D",
        start_marker_col="2023 Q3 ACT YTD FINAL",
        start_marker_val="2023 Q4 ACT YTD FLASH",
        source_col="Unnamed: 4",
        keyword_col="Unnamed: 0"
    )

def summarize_pqcop(final_percentage_by_category):
    
    fix_df = final_percentage_by_category[
        (final_percentage_by_category["VAR/FIX"] == "FIX") &
        (final_percentage_by_category["Category"] != "R&D")
    ]

    var_sum = final_percentage_by_category[final_percentage_by_category["VAR/FIX"] == "VAR"][
        ["CLA (%)", "LWR (%)", "MID (%)", "UPR (%)"]
    ].sum()

    fix_sum = fix_df[["CLA (%)", "LWR (%)", "MID (%)", "UPR (%)"]].sum()

    rd_row = final_percentage_by_category[final_percentage_by_category["Category"] == "R&D"][
        ["CLA (%)", "LWR (%)", "MID (%)", "UPR (%)"]
    ]

    if rd_row.empty:
        rd_values = [0, 0, 0, 0]
    else:
        rd_values = rd_row.iloc[0].tolist()

    summary_pqcop = pd.DataFrame({
        "Category": ["VAR", "FIX", "R&D"],
        "CLA (%)": [var_sum["CLA (%)"], fix_sum["CLA (%)"], rd_values[0]],
        "LWR (%)": [var_sum["LWR (%)"], fix_sum["LWR (%)"], rd_values[1]],
        "MID (%)": [var_sum["MID (%)"], fix_sum["MID (%)"], rd_values[2]],
        "UPR (%)": [var_sum["UPR (%)"], fix_sum["UPR (%)"], rd_values[3]],
    })

    return summary_pqcop
