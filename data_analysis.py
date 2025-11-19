import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
PATH_2015 = "data/FD_LOGEMTZA_2015_small.csv"
df_2015 = pd.read_csv(PATH_2015, sep=';', low_memory=False)



dico_df = {2015: df_2015}
result2 = pd.DataFrame(columns=['Fioul', 'Gaz de ville'])


for year in dico_df:
    df = dico_df[year]
    result2.loc[year] = [int((df_2015['CMBL'] == 3).sum()), int((df_2015['CMBL'] == 2).sum())]


print(result2)