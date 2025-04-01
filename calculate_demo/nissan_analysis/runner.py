import os
import pandas as pd

from .io import load_all_data
from .bop import process_bop
from .finalizer import build_final_summary
from .pxp import fill_pxp_values
from .logistics import fill_logistics
from .pqcop import fill_pqcop_values, summarize_pqcop
from .percentage import compute_percent_by_category
from .display import display
from .filters import fill_from_summary_results

def run_all(paths_dict):
    df_bop, df_pxp, df_pqcop, df_logistic, df_scrap = load_all_data(paths_dict)
    summary_results, weighted_summary, unweighted_summary, final_summary = process_bop(df_bop)
    final_summary = build_final_summary(df_pxp, df_scrap, summary_results, weighted_summary, unweighted_summary, final_summary)

    cost_map = {
        "TRANSMISSION LOCAL": "Local",
        "TRANSMISSION KD": "KD"
    }
    fill_from_summary_results(
        summary_results=summary_results,
        final_summary=final_summary,
        cost_group_to_desc_map=cost_map,
        trim_column="SL AWD",
        target_category="Total Transmission"
    )

    fill_pxp_values(df_pxp, final_summary)
    fill_logistics(df_logistic, final_summary)
    fill_pqcop_values(df_pqcop, final_summary)

    try:
        bop_rows = final_summary[
            (final_summary["TDC"] == "BOP") &
            (final_summary["Description"] != "Total Summary")
        ]
        sums = bop_rows[["CLA", "LWR", "MID", "UPR"]].sum()
        final_summary.loc[
            final_summary["Category"] == "Total BOP",
            ["CLA", "LWR", "MID", "UPR"]
        ] = sums.values
    except:
        pass

    try:
        total_rows = final_summary[final_summary["Description"] == "Total Summary"]
        tdc_sum = total_rows[["CLA", "LWR", "MID", "UPR"]].sum()
        total_row = {
            "Category": "Total TDC",
            "Description": "Grand Total of All TDC Sections",
            "VAR/FIX": "Total",
            "TDC": "TDC",
            "VEH/ENG": "All",
            "CLA": tdc_sum["CLA"],
            "LWR": tdc_sum["LWR"],
            "MID": tdc_sum["MID"],
            "UPR": tdc_sum["UPR"]
        }
        final_summary.loc[len(final_summary)] = total_row
    except:
        pass

    display("final summary", final_summary)
    final_percentage = compute_percent_by_category(final_summary)
    display("output-cost group", final_percentage)

    try:
        summary_pqcop = summarize_pqcop(final_percentage)
        display("pqcop", summary_pqcop)
    except:
        summary_pqcop = None

    try:
        output_dir = paths_dict.get("output_dir", "./outputs")
        os.makedirs(output_dir, exist_ok=True)

        final_summary.to_csv(os.path.join(output_dir, "final_summary.csv"), index=False)
        final_percentage.to_csv(os.path.join(output_dir, "output_cost_group.csv"), index=False)

        if summary_pqcop is not None:
            summary_pqcop.to_csv(os.path.join(output_dir, "pqcop.csv"), index=False)

        print(f"✅ CSV files saved to {output_dir}")
    except Exception as e:
        print(f"⚠️ Failed to save CSV files: {e}")

generate_all_tables = run_all

