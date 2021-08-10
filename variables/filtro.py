import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from variables.tabela_var import a_avr2
from variables.tabela_ques import a_ques
from variables.tabela_relato import relaa

# Funções
def reorder_columns(dataframe, col_name, position):
    """Reorder a dataframe's column.
    Args:
        dataframe (pd.DataFrame): dataframe to use
        col_name (string): column name to move
        position (0-indexed position): where to relocate column to
    Returns:
        pd.DataFrame: re-assigned dataframe
    """
    temp_col = dataframe[col_name]
    dataframe = dataframe.drop(columns=[col_name])
    dataframe.insert(loc=position, column=col_name, value=temp_col)
    return dataframe

#  Tabela variações

a_avr=a_avr2.copy()

aux_a_var=a_avr.columns.values.tolist()
aux_a_var.remove("namespace")


l_media_var=pd.DataFrame()

for col in aux_a_var:
    lista_mean=list()
    m=float("{:.2f}".format((a_avr[col].mean())*100))
    #m=str(m)+'%'
    lista_mean.append(m)
    s=pd.DataFrame(lista_mean)
    l_media_var[col]= s.sum()

l_media_var["namespace"]='Media SC-Eduqo'
l_media_var=reorder_columns(l_media_var, 'namespace', 0)

# Arrumando dataframe de variações para mostrar após filtro
a_var3=a_avr2.copy()
for col in aux_a_var:
    z=(a_var3[col]*100).round(2)#.astype(str)+'%'
    a_var3.loc[:,col]=z

# pegando df de questões e renomeando colunas

a_ques2=a_ques.copy()
nomemetricas=['Métrica Questões','Métrica Discursivas','Métrica Banco','Métrica Banco Discursivas']
a_quescolum=a_ques2.columns.values.tolist()
a_quescolum.remove("namespace")
i=0

for col in a_quescolum:
    n=nomemetricas[i]
    a_ques2=a_ques2.rename(columns={col: n})
    i+=1

#  Tabela questões

aux_a_ques=a_ques2.columns.values.tolist()
aux_a_ques.remove("namespace")


l_media_ques=pd.DataFrame()

for col in aux_a_ques:
    lista_mean1=list()
    mq=float("{:.2f}".format((a_ques2[col].mean())))
    #m=str(m)+'%'
    lista_mean1.append(mq)
    sq=pd.DataFrame(lista_mean1)
    l_media_ques[col]= sq.sum()

l_media_ques["namespace"]='Media SC-Eduqo'
l_media_ques=reorder_columns(l_media_ques, 'namespace', 0)

#  Tabela rela

relaa2=relaa.copy()


aux_a_relaa2=relaa2.columns.values.tolist()
aux_a_relaa2.remove("namespace")


l_media_relaa2=pd.DataFrame()

for col in aux_a_relaa2:
    lista_meanr=list()
    mr=float("{:.2f}".format((relaa2[col].mean())))
    #m=str(m)+'%'
    lista_meanr.append(mr)
    s=pd.DataFrame(lista_meanr)
    l_media_relaa2[col]= s.sum()

l_media_relaa2["namespace"]='Media SC-Eduqo'
l_media_relaa2=reorder_columns(l_media_relaa2, 'namespace', 0)
