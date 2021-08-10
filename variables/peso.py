import pandas as pd
import time
import numpy as np
from datetime import date, timedelta
import plotly.express as px


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


df_pesos=pd.read_csv('pesos.csv').reset_index(drop=True)

# Copiando dataframe
pesos=df_pesos.copy()
#pegando todos os nomes de colunas
colunas=df_pesos.columns.values.tolist()

# criando váriaveis
lista=list()
irrelevante = pd.DataFrame()

# abrindo para cada coluna
for col in colunas:
    #variaveis internas
    cont=0
    lista=list()
    # correndo agora a coluna inteira e verificando
    # se temos os Args que queremos
    for i in (range(len(pesos[col]))):
        aux=pesos[col][i]
        if aux == 'Discordo' or aux == 'Discordo plenamente':
            cont=1
        else:
            cont=0
        lista.append(cont)
    var=pd.DataFrame(lista)
    irrelevante[col]=var.sum()

# agora retirando as váriaveis que nao são relevantes do dataframe

lista_irrelevantes=list()

for col in colunas:
    for i in (range(len(irrelevante[col]))):
        aux=irrelevante[col][i]
        if aux >= 5:
            lista_irrelevantes.append(col)

variavel=lista_irrelevantes


#print('\tAs variaveis irrelevantes são : ',variavel)
pesos=pesos.drop(variavel, axis=1)

pesos_final=pesos.copy()

colunas_2=pesos_final.columns.values.tolist()
colunas_2.remove('Endereço de e-mail')
lista_trans=list()

variavel_concordo_plenamente = 1
variavel_concordo = 0.5
variavel_neutro = 0.1
variavel_discordo = 0


for col in colunas_2:
    for i in (range(len(pesos_final[col]))):
        aux_trans=pesos_final[col][i]
        if aux_trans == 'Concordo plenamente':
            pesos_final[col][i]= variavel_concordo_plenamente
        elif aux_trans == 'Concordo':
            pesos_final[col][i]=variavel_concordo
        elif aux_trans == 'Neutro':
            pesos_final[col][i]=variavel_neutro
        else:
            pesos_final[col][i]=variavel_discordo


mult_lider=1.1
multi_normal=1

pesos_final_final=pesos_final.copy()

coluna = 'Endereço de e-mail'
aux=0
for i in range(len(pesos_final[coluna])):
    aux = pesos_final[coluna][i]
    if aux == 'amanda' or  aux == 'magnum.santos' or aux =='cassiano':
        mult=mult_lider
    else:
        mult=multi_normal
    for col in colunas_2:
        aux_mult=pesos_final_final[col][i] * mult
        pesos_final_final[col][i]=aux_mult



media= pd.DataFrame()
for col in colunas_2:
    lista_media=list()
    aux_media=pesos_final_final[col].sum()/len(pesos_final_final[col])
    lista_media.append(aux_media)
    var_media=pd.DataFrame(lista_media)
    media[col]=var_media.sum()

media_var=media.iloc[:,0:5].round(2)
media_quest=media.iloc[:,5:9].round(2)
media_rela=media.iloc[:,9:].round(2)
