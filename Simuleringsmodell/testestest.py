import pandas as pd
from stue import Stue
df_1 = pd.read_excel("/Users/sabinal/Desktop/MASTER 2022/DATA/Python kode/ferdigbehandletinput.xls")

df_2 = pd.read_excel("/Users/sabinal/Desktop/MASTER 2022/Hospital_similation/Simuleringsmodell/ferdigbehandletoutput.xls")

missing_patient = []


if __name__ == '__main__':

    for i in range(1,5):
        print(i)