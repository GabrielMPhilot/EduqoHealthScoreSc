import pandas as pd
import time
import numpy as np
from datetime import date, timedelta
import plotly.express as px
from variables.peso import media_var

# importando tabela de variações

df_var=pd.read_csv('tabela_variacoes_pesos.csv').reset_index(drop=True)
df_var=df_var.drop(df_var.columns[[0,7,8]], axis=1)

a_avr2=df_var.copy()

# normalizando

var=df_var.copy()

# pegando valor max() de cada

aux_var=var.columns.values.tolist()
aux_var.remove('namespace')

aux_var_max=list()
aux_var_min=list()
for col in aux_var:
    aux_mx=var[col].max()
    aux_mi=var[col].min()
    aux_var_max.append(aux_mx)
    aux_var_min.append(aux_mi)

# Dividindo colunas pelo valor max() para normalização

for i in range(len(aux_var_max)):
    var[aux_var[i]]=(var[aux_var[i]]-aux_var_min[i])/(aux_var_max[i]-aux_var_min[i])


# Mult pesos para fazer a soma e o sort by

aux_df_var=df_var.columns.values.tolist()
aux_df_var.remove('namespace')
aux_media_var=media_var.values.tolist()


tabela_var=var.copy()
i=0
for col in aux_df_var:
    tabela_var[col]=(tabela_var[col] * aux_media_var[0][i]).round(2)
    i+=1

tabela_var2=tabela_var.copy()

tabela_var["soma"]=tabela_var.sum(axis=1, numeric_only=True)
tabela_var=tabela_var.sort_values(by="soma").reset_index(drop=True)
#tabela_var
