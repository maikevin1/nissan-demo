# fillers.py
import pandas as pd

def fill_from_summary_results(
    summary_results,
    final_summary,
    cost_group_to_desc_map,
    trim_column,
    target_category
):
    for cost_group, desc in cost_group_to_desc_map.items():
        try:
            value = summary_results.loc[
                summary_results["COST GROUP"] == cost_group,
                trim_column
            ].values[0]
        except IndexError:
            value = 0

        mask = (
            (final_summary["Category"] == "VAR T/M") &
            (final_summary["Description"] == desc)
        )
        final_summary.loc[mask, ["CLA","LWR","MID","UPR"]] = value

    rows = final_summary[
        (final_summary["Category"]=="VAR T/M") &
        (final_summary["Description"]!="Total Summary")
    ]
    sums = rows[["CLA","LWR","MID","UPR"]].sum()
    final_summary.loc[
        final_summary["Category"]==target_category,
        ["CLA","LWR","MID","UPR"]
    ] = sums.values
