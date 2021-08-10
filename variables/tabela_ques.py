import pandas as pd
import time
import numpy as np
from datetime import date, timedelta
import plotly.express as px
from variables.peso import media_quest

# importando tabela de questões

df_quest=pd.read_csv('tabela_questoes.csv').reset_index(drop=True)
df_quest=df_quest.drop(df_quest.columns[[0,4]], axis=1)

a_ques=df_quest.copy()

# normalizando

quest=df_quest.copy()

# pegando valor max() de cada

aux_var=quest.columns.values.tolist()
aux_var.remove('namespace')

aux_var_max1=list()
aux_var_min1=list()
for col in aux_var:
    aux_mx1=quest[col].max()
    aux_min1=quest[col].min()
    aux_var_max1.append(aux_mx1)
    aux_var_min1.append(aux_min1)

# Dividindo colunas pelo valor max() para normalização

for i in range(len(aux_var_max1)):
    quest[aux_var[i]]=(quest[aux_var[i]]-aux_var_min1[i])/(aux_var_max1[i]-aux_var_min1[i])


# Mult pesos para fazer a soma e o sort by

aux_df_quest=quest.columns.values.tolist()
aux_df_quest.remove('namespace')
aux_media_quest=media_quest.values.tolist()


tabela_quest=quest.copy()
i=0
for col in aux_df_quest:
    tabela_quest[col]=(tabela_quest[col] * aux_media_quest[0][i]).round(2)
    i+=1
tabela_quest2=tabela_quest.copy()
tabela_quest["soma"]=tabela_quest.sum(axis=1, numeric_only=True)
tabela_quest=tabela_quest.sort_values(by="soma").reset_index(drop=True)
