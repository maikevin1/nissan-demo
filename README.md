# 📊 Nissan Cost Analysis Pipeline

This project provides a complete and automated cost analysis system for Nissan's cost breakdown data, including BOP, PXP, PQCOP, logistics, R&D, and transmission costs. It loads all input datasets, processes them, and generates three final outputs: a **cost summary table**, **cost group percentage table**, and a **PQCoP summary** — all exportable as `.csv` files.

---

## 🔧 Features

- ✅ Full integration of BOP, PXP, PQCOP, Logistics, and Scrap cost data  
- ✅ Smart handling of function dependencies and normalization (e.g. Local/KD logic for Transmission)  
- ✅ Automatic aggregation: `Total BOP`, `Total TDC`, and other summaries  
- ✅ Column-wise percentage breakdown for CLA/LWR/MID/UPR  
- ✅ Final export to CSV for all key tables  
- ✅ Easy-to-use one-line execution: `generate_all_tables(paths_dict)`

---

## 📁 Folder Structure

nissan_analysis/ ├── init.py ├── runner.py # Main controller ├── io.py # Input file loader ├── bop.py # BOP logic & FD extraction ├── finalizer.py # Final summary table builder ├── pxp.py # PXP section filling ├── logistics.py # Logistic cost filler ├── pqcop.py # R&D + PQCOP logic ├── percentage.py # Percentage calculator ├── display.py # Helper for table display ├── filters.py # Custom rules (e.g., Local/KD value mapping)


---

## 📥 Input Files

The following CSV files are required as inputs:

- `sheet-bop.csv`
- `sheet-pxp.csv`
- `sheet-pqcop.csv`
- `sheet-logistics.csv`
- `sheet-RD - Scrap.csv`

All files must contain properly formatted cost group and trim-level cost breakdowns.

---

## 🚀 How to Run

### 1. Import the runner

```python
from nissan_analysis.runner import generate_all_tables

### 2. Prepare the file paths

paths = {
    "bop": "/path/to/sheet-bop.csv",
    "pxp": "/path/to/sheet-pxp.csv",
    "pqcop": "/path/to/sheet-pqcop.csv",
    "logistic": "/path/to/sheet-logistics.csv",
    "scrap": "/path/to/sheet-RD - Scrap.csv",
    "output_dir": "/path/to/output/folder"  # CSV files will be saved here
}

### 3. run
generate_all_tables(paths)
