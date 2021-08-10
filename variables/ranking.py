import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from variables.tabela_var import tabela_var2
from variables.tabela_ques import tabela_quest2
from variables.tabela_relato import tabela_rela2

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



# Importando tabelas para uniao

a_tabela_var = tabela_var2.copy()
a_tabela_ques =tabela_quest2.copy()
a_tabela_rela =tabela_rela2.copy()

# Unindo em uma tabela e realizando a soma

tabela_rank=pd.merge(a_tabela_var, a_tabela_ques, on=["namespace"], how='outer')
tabela_rank=pd.merge(tabela_rank, a_tabela_rela, on=["namespace"], how='outer')
tabela_rank["soma"]=tabela_rank.sum(axis=1, numeric_only=True)
tabela_rank=tabela_rank.sort_values(by="soma").reset_index(drop=True)

# Pegando os quartil's

quartil=tabela_rank.copy().round(2)
quartil=reorder_columns(quartil, 'soma', 1)
quartil=quartil.iloc[:,0:2]

coluna="soma"



q=(quartil[coluna].max()-quartil[coluna].min())/4

m=quartil[coluna].min()
quartil["quartil"]=0
quartil["Risco"]=0
for i in range(len(quartil[coluna])):
    ax=0
    b=0
    aux_q = quartil[coluna][i]
    #print(aux_q)
    if aux_q >= m and aux_q < m + q:
        ax=4
        b="Alto Risco"
    elif aux_q >= m+q and aux_q < m + 2*q:
        ax=3
        b="Risco"
    elif aux_q >= m+2*q and aux_q < m + 3*q:
        ax=2
        b="Neutro"
    else:
        ax=1
        b="Bom uso"
    #print(ax)
    quartil.loc[i,"quartil"]=ax
    quartil.loc[i,"Risco"]=b

ns_quartil=quartil.copy()
# Arrumando Df

quartil=quartil.groupby(['Risco'])[['quartil']].count().reset_index()
quartil=quartil.rename(columns={"quartil": "Quantidade de escolas"})
q_por=quartil['Quantidade de escolas'].sum()

aux_quartil_teste=quartil.copy()
aux_quartil_teste["Porcentagem"]=((aux_quartil_teste["Quantidade de escolas"]/q_por)*100).round(2)

# Ordenando Df

aux_quartil_teste['ordem']=0
for i in range(len(aux_quartil_teste['Risco'])):
    b=0
    a=aux_quartil_teste['Risco'][i]
    if a =='Alto Risco':
        b=int(1)
    elif a =='Risco':
        b=int(2)
    elif a =='Neutro':
        b=int(3)
    elif a =='Bom uso':
        b=int(4)
    aux_quartil_teste.loc[i,"ordem"]=b
aux_quartil_teste=aux_quartil_teste.sort_values(by="ordem", ascending=True).reset_index(drop=True)

# numero total de escolas

aux_card_total=aux_quartil_teste["Quantidade de escolas"].sum()

# porcentagem de escolas no grupo de risco

aux_card_porcen=aux_quartil_teste.iloc[0:2,:]
aux_card_porcen=aux_card_porcen["Porcentagem"].round(2).sum()#.astype(str)+' %'
aux_quartil_teste["Porcentagem"]=aux_quartil_teste["Porcentagem"].astype(str)+'%'

# Parte para selecão no front

# df namespace e risco
ns_quartil=reorder_columns(ns_quartil, 'Risco', 1)
ns_quartil=ns_quartil.iloc[:,0:2]

# lista namesapces
namespace_list=ns_quartil["namespace"].values.tolist()
# lista graus de risco
graurisco_list=ns_quartil["Risco"].drop_duplicates().values.tolist()
