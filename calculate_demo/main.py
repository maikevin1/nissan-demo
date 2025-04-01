# %%
from nissan_analysis.runner import generate_all_tables
from nissan_analysis.display import display

bop_path = "/Users/kevin/Desktop/nissan-data/sheet-bop.csv"
pxp_path = "/Users/kevin/Desktop/nissan-data/sheet-pxp.csv"
pqcop_path = "/Users/kevin/Desktop/nissan-data/sheet-pqcop.csv"
logistic_path = "/Users/kevin/Desktop/nissan-data/sheet-logistic.csv"
scrap_path = "/Users/kevin/Desktop/nissan-data/sheet-RD - Scrap.csv"

tables = generate_all_tables(
    bop_path=bop_path,
    pxp_path=pxp_path,
    pqcop_path=pqcop_path,
    logistic_path=logistic_path,
    scrap_path=scrap_path
)

display("Final Summary", tables["final_summary"])
display("Cost Group %", tables["cost_group_percent"])
display("PQCoP Summary", tables["pqcop_summary"])
