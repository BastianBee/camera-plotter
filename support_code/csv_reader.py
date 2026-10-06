import pandas as pd

from pathlib import Path


def dat_reader(filename):
    return pd.read_csv(filename, header=None, sep=r'\s+')

def csv_reader(filename):
    return pd.read_csv(filename, header=None)




