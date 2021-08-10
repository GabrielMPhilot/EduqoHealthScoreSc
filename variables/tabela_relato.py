import pandas as pd
import time
import numpy as np
from datetime import date, timedelta
import plotly.express as px
from variables.peso import media_rela


df_rela=pd.read_csv('tabela_relatorios.csv').reset_index(drop=True)
df_rela=df_rela.drop(df_rela.columns[[0]], axis=1)

relaa=df_rela.copy()

# normalizando

rela=df_rela.copy()

# pegando valor max() de cada

aux_var=rela.columns.values.tolist()
aux_var.remove('namespace')

aux_var_max2=list()
aux_var_min2=list()
#print(aux_var_min)
for col in aux_var:
    aux_mx2=rela[col].max()
    aux_mi2=rela[col].min()
    aux_var_max2.append(aux_mx2)
    aux_var_min2.append(aux_mi2)

# Dividindo colunas pelo valor max() para normalização

for i in range(len(aux_var_max2)):
    rela[aux_var[i]]=(rela[aux_var[i]]-aux_var_min2[i])/(aux_var_max2[i]-aux_var_min2[i])


# Mult pesos para fazer a soma e o sort by

aux_df_rela=rela.columns.values.tolist()
aux_df_rela.remove('namespace')
aux_media_rela=media_rela.values.tolist()


tabela_rela=rela.copy()
i=0
for col in aux_df_rela:
    tabela_rela[col]=(tabela_rela[col] * aux_media_rela[0][i]).round(2)
    i+=1

tabela_rela2=tabela_rela.copy()
tabela_rela["soma"]=tabela_rela.sum(axis=1, numeric_only=True)
tabela_rela=tabela_rela.sort_values(by="soma").reset_index(drop=True)
