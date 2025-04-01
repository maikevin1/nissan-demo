# 📊 Nissan Cost Analysis Pipeline

This project provides a complete and automated cost analysis system for Nissan's cost breakdown data. It loads all input datasets, processes them, and generates three final outputs: a **cost summary table**, **cost group percentage table**, and a **final summary** — all exportable as `.csv` files.

---

## 🔧 Features

- ✅ Full integration data  
- ✅ Smart handling of function dependencies and normalization (e.g. Local/KD logic for Transmission)  
- ✅ Automatic aggregation: `Total cost`, `Total summary`, and other summaries  
- ✅ Column-wise percentage breakdown for CLA/LWR/MID/UPR  
- ✅ Final export to CSV for all key tables  
- ✅ Easy-to-use one-line execution: `generate_all_tables(paths_dict)`


## 🚀 How to Run

### 1. Import the runner

```python
from nissan_analysis.runner import generate_all_tables
```
### 2. Prepare the file paths

```python
paths = {
    "bop": "/path/to/sheet-bop.csv",
    "pxp": "/path/to/sheet-pxp.csv",
    "pqcop": "/path/to/sheet-pqcop.csv",
    "logistic": "/path/to/sheet-logistics.csv",
    "scrap": "/path/to/sheet-RD - Scrap.csv",
    "output_dir": "/path/to/output/folder"  # CSV files will be saved here
}
```

### 3. run
```python
generate_all_tables(paths)
```
