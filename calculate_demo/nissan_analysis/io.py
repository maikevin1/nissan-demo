
import pandas as pd

def load_all_data(paths):
    df_bop = pd.read_csv(paths['bop'])
    df_pxp = pd.read_csv(paths['pxp'], encoding='latin1')
    df_pqcop = pd.read_csv(paths['pqcop'])
    df_logistic = pd.read_csv(paths['logistics'])
    df_scrap = pd.read_csv(paths['scrap'])
    return df_bop, df_pxp, df_pqcop, df_logistic, df_scrap
