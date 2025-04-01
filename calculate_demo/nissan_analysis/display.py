
from tabulate import tabulate

def display(name, dataframe):
    print(f"\n== {name} ==")
    print(tabulate(dataframe, headers='keys', tablefmt='psql', showindex=False))
