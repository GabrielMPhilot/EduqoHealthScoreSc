# Importando bibliotecas

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from variables.tabela_var import tabela_var, a_avr2
from variables.tabela_relato import relaa
from variables.ranking import aux_card_porcen,aux_quartil_teste,aux_card_total, ns_quartil, namespace_list, graurisco_list,name_quartil
from variables.filtro import l_media_var, a_var3, l_media_ques, l_media_relaa2, a_ques2
from PIL import Image
import plotly.graph_objects as go
import time
import matplotlib.pyplot as plt
import matplotlib
import base64

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
def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="listanamespaces.csv">Clique aqui para baixar o CSV</a>'
    return href

# !!!adicionar grau de risco para quando selecionar o namespace
# Colocando imagem em cima

st.image('[LOGO] Eduqo.png')

# Titulo


"""
# 🌡️ Health Score SC - Produto padre jow
#### Projeto utilizando apenas escolas do Sucesso do cliente.

"""

# Side bar
## Imagem na side bar
image = Image.open('[LOGO] Eduqo.png')
st.sidebar.image(image,caption='Eduqo - Plataforma QMágico',use_column_width=True)

st.sidebar.markdown('Feito por: Gabriel Philot (Tio Gibbs)')
st.sidebar.write('#### Material de apoio, caso queira saber mais sobre o projeto.')
st.sidebar.write('####')
st.sidebar.write("###### Forms:  [link](https://docs.google.com/forms/d/e/1FAIpQLSfmUHHnNu8wiMH2W6UuBQS354UL25D_ZIDstYqvMj7bLSs4vA/viewform)")
st.sidebar.write("##### Docs:  [link](https://docs.google.com/document/d/1bdASwpnSDREVDR0TwKtcvcxNL4AFz-xR5WSNNTa-hwM/edit)")
st.sidebar.write("##### Github:  [link](https://github.com/GabrielMPhilot/EduqoHealthScoreSc)")
st.sidebar.write('#')
st.sidebar.write('#### Resultado da classificação de nosso modelo:',get_table_download_link(name_quartil), unsafe_allow_html=True)


# Grande ideia

"""
### 💡 Grande ideia do Projeto
O objetivo desse projeto é criar um HealthScore escalavel e preciso sobre nossos clientes.
Utilizamos primeiramente dados diversos da usabilidade do Produto (por enquanto), para criarmos
métricas que consigam mapear se nossos clientes estão utilizando a plataforma de maneira adequada,
com as métricas é formado um modelo para Rankear cada escola em um grau de risco especifico.

### 💾 Dados utilizados
Os dados utilizados foram segmentados (por enquanto) em 3 diferentes tabelas.
"""
"""
#### 1. Tabela de Variações:
Essa tabela contempla dados de variação do n° de alunos, variação do n° A.A's subidas (proffs),
variação do n° de interação de alunos em A.A's, variação do n° de conteúdos em caderno subidos (proffs) e
variação do n° de interação de alunos em conteúdos do caderno. O intervalo de extração desses dados é de
dados de  **01/03/2020 até 01/08/2020 e  01/03/2021 até 01/08/2021**.

#### 2. Tabela de Questões:
Essa Tabela contempla dados do n° de questões totais subidas(proffs/admin), n° de questões discursivas subidas(proffs/admin),
n° de questões totais do banco subidas (proffs/admin), n° de questões discursivas do banco subidas (proffs/admin). O intervalo de extração desses dados é de
dados de  **01/01/2021 até 01/08/2021**.
#### 3. Tabela de Relatórios:
Essa Tabela contempla dados do n° de vizualização de relátorios (proffs/admin) de A.A's, n° de vizualização de relátorios (proffs/admin) de S.Exs,
n° de vizualização de relátorios (proffs/admin) de Cadernos, n° de vizualização de relátorios (proffs/admin) de AD's, n° de vizualização de relátorios (proffs/admin) Mensais (QBR,Mensal). O intervalo de extração desses dados é de
dados de  **01/01/2021 até 01/08/2021**.
"""
"""
### 🔍 Certo agora vamos para os **Resultados**.

"""

# Colando n° total e Porcentagem
#aux_card_porcen - Porcentagem
#aux_card_total - Quantidade

figa = go.Figure()

figa.add_trace(go.Indicator(
    #mode = "number+delta",
    value = aux_card_total ,
    domain = {'x': [0.25, 0.75], 'y': [0.7, 1]},
    title = {"text": "N° de escolas analisadas<br><span style='font-size:0.8em;color:gray'>"}))
    ##delta = {'reference': 400, 'relative': True, 'position' : "top"}))
figa.add_trace(go.Indicator(
    #mode = "number+delta",
    value = aux_card_porcen,
    domain = {'x': [0.25, 0.75], 'y': [0, 0.3]},
    title = {"text": "<span style='font-size:1em;color:red'>%<br><span style='font-size:0.8em;color:red'>de escolas em Risco</span><br>"}))
    ##delta = {'reference': 400, 'relative': True, 'position' : "top"}))
st.plotly_chart(figa)



# Gráfico do Health Score - Pontuação via nosso modelo
fig =px.bar(aux_quartil_teste, x='Risco', y='Quantidade de escolas',
           color='Risco',
           color_discrete_sequence=["#E45756","#F58518","#54A24B","#4C78A8"],
           #color_discrete_sequence=px.colors.qualitative.T10,
            text=aux_quartil_teste['Porcentagem'])


fig.update_xaxes(showgrid=False)
fig.update_layout(title = "Distribuição no N° de escolas por grau de Risco")

st.plotly_chart(fig)
"""
"""
left_column, right_column = st.columns(2)
pressed = right_column.button('Download Resultado')
if pressed:
    left_column.write(get_table_download_link(name_quartil), unsafe_allow_html=True)
#st.markdown(get_table_download_link(name_quartil), unsafe_allow_html=True)
"""
##### Com o rankeamento de risco, podemos olhar as escolas que estão em perigo e aquelas
##### que estão fazendo um bom uso, de acordo com suas métricas.

"""
"""

"""
expander = st.expander("OBS Métricas -> (clique aqui 🖱️)")
expander.write("(1.1) As Métricas que serão apresentadas a seguir, foram tratadas e modeladas para formar o ranking, porém serão mostradas de forma 'Bruta' para conseguirmos comparar as diferenças com mais facilidade. (1.2) A Média apresentada das escolas também são as médias 'Brutas'.")
expander.write("(2.1) Nas tabelas com mapa de calor os valores máximos (mais escuros) não são globais, ou seja se referem ao valor máximo da tabela selecionada pelo filtro, a não ser que a escolha de filtro seja todos os namespaces. ")
expander.write("(2.2) Nas visualizações por Grau de Risco e Todos os namespaces, o valor de risco apresentado nas tabelas é referente a pontuação de nosso modelo, então não necessariamente o valor de uma determinada tabela é o que faz a escola estar em risco ou não.")
"""

"""
"""
Agora para visualização das Métricas
"""
####################################### FILTRO ##############################
aux_filtro_show=0
a_dict=0
genre = st.radio(
 "Escolha o tipo de filtro.",
('Grau de Risco', 'Namespace','Todos os Namespaces'))

if genre == 'Namespace':

    #st.write('Escolha agora o  ',genre)
    select = st.selectbox('Namespace', namespace_list, key='2')
    #st.write('O Namespace selecionada foi : ',select)
    aux_filtro_show=1
    a_dict=0
    namevar=a_var3.copy()
    nameques=a_ques2.copy()
    namerela=relaa.copy()

    ######## Tabela variações
    filtrovar=namevar[(namevar["namespace"] == select)]
    filtrovar=l_media_var.append(filtrovar).reset_index(drop=True)#.transpose().reset_index()


    #arrumando tabela para plot gráfico
    aux_filtrovar=filtrovar.copy()
    a_filtrovar=aux_filtrovar.columns.values.tolist()
    a_filtrovar.remove('namespace')
    filtrovar_aux=pd.DataFrame()
    for col in a_filtrovar:
        for i in range(len(aux_filtrovar[col])):
            var_ns=aux_filtrovar.loc[i,"namespace"]
            var_variav=col
            var_valor=aux_filtrovar.loc[i, col]
            var_porcent=str(aux_filtrovar.loc[i, col])+'%'
            new_row={'Namespace': var_ns, 'Métricas': col, 'Valor': var_valor, 'Porcentagem': var_porcent}
            filtrovar_aux=filtrovar_aux.append(new_row, ignore_index=True)

    #plot gráfico varições
    figvar =px.bar(filtrovar_aux, x='Valor', y='Métricas',
               color='Namespace',orientation='h',
               color_discrete_sequence=["rgb(102, 197, 204)","rgb(248, 156, 116)"],#"#54A24B","#4C78A8"],
               #color_discrete_sequence=px.colors.qualitative.T10,
                text=filtrovar_aux['Porcentagem'])


    figvar.update_xaxes(showgrid=False)
    figvar.update_layout(title = "Métricas na Tabela de Variação")

    ########## Tabela questoes
    filtroques=nameques[(nameques["namespace"] == select)]
    filtroques=l_media_ques.append(filtroques).reset_index(drop=True)#.transpose().reset_index()


    #arrumando tabela para plot gráfico
    aux_filtroques=filtroques.copy()
    a_filtroques=aux_filtroques.columns.values.tolist()
    a_filtroques.remove('namespace')
    a_filtroques_aux=pd.DataFrame()
    for col in a_filtroques:
        for i in range(len(aux_filtroques[col])):
            ques_ns=aux_filtroques.loc[i,"namespace"]
            ques_variav=col
            ques_valor=aux_filtroques.loc[i, col]
            ques_porcent=str(aux_filtroques.loc[i, col])+'%'
            new_rowq={'Namespace': ques_ns, 'Métricas': col, 'Valor': ques_valor, 'Porcentagem': ques_porcent}
            a_filtroques_aux=a_filtroques_aux.append(new_rowq, ignore_index=True)

    #plot gráfico questoes
    figques =px.bar(a_filtroques_aux, x='Valor', y='Métricas',
               color='Namespace',orientation='h',
               color_discrete_sequence=["rgb(102, 197, 204)","rgb(248, 156, 116)"],#"#54A24B","#4C78A8"],
               #color_discrete_sequence=px.colors.qualitative.T10,
                text=a_filtroques_aux['Valor'])


    figques.update_xaxes(showgrid=False)
    figques.update_layout(title = "Métricas na Tabela de Questões")

    ########## Tabela relatorios
    filtrorela=namerela[(namerela["namespace"] == select)]
    filtrorela=l_media_relaa2.append(filtrorela).reset_index(drop=True)#.transpose().reset_index()


    #arrumando tabela para plot gráfico
    aux_filtrorela=filtrorela.copy()
    a_filtrorela=aux_filtrorela.columns.values.tolist()
    a_filtrorela.remove('namespace')
    a_filtrorela_aux=pd.DataFrame()
    for col in a_filtrorela:
        for i in range(len(aux_filtrorela[col])):
            rel_ns=aux_filtrorela.loc[i,"namespace"]
            rel_variav=col
            rel_valor=aux_filtrorela.loc[i, col]
            rel_porcent=str(filtrorela.loc[i, col])+'%'
            new_rowr={'Namespace': rel_ns, 'Métricas': col, 'Valor': rel_valor, 'Porcentagem': rel_porcent}
            a_filtrorela_aux=a_filtrorela_aux.append(new_rowr, ignore_index=True)

    #plot gráfico rela
    figrel =px.bar(a_filtrorela_aux, x='Valor', y='Métricas',
               color='Namespace',orientation='h',
               color_discrete_sequence=["rgb(102, 197, 204)","rgb(248, 156, 116)"],#"#54A24B","#4C78A8"],
               #color_discrete_sequence=px.colors.qualitative.T10,
                text=a_filtrorela_aux['Valor'])


    figrel.update_xaxes(showgrid=False)
    figrel.update_layout(title = "Métricas na Tabela de Relátorios")


elif genre =='Grau de Risco':
    #st.write('Escolha agora o  ',genre)
    select = st.selectbox('Grau de Risco', graurisco_list, key='2')
    #st.write('O Grau de risco selecionad foi : ',select)
    aux_filtro_show=0
    a_dict=0
    namevar=a_var3.copy()
    nameques=a_ques2.copy()
    namerela=relaa.copy()

    ######## Variavel de filtro
    aux_filtro=ns_quartil[(ns_quartil["Risco"] == select)]
    aux_filtro=aux_filtro["namespace"]

    ######## Tabela variações

    filtro_var=namevar[namevar['namespace'].isin(aux_filtro)]
    #cl_aux=filtro_var.columns.values.tolist()
    #cl_aux.remove("namespace")
    #for col in cl_aux:
        #filtro_var.loc[:,col]=filtro_var[col].astype(str)+'%'
    filtro_var=filtro_var.reset_index(drop=True)
    ######## Tabela quest

    filtro_ques=nameques[nameques['namespace'].isin(aux_filtro)].reset_index(drop=True)

    ######## Tabela rela

    filtro_rela=namerela[namerela['namespace'].isin(aux_filtro)].reset_index(drop=True)
else:
    st.write(genre, 'foram selecionados.')
    aux_filtro_show=0
    a_dict=1
    namevar=a_var3.copy()
    nameques=a_ques2.copy()
    namerela=relaa.copy()

    ######## Tabela variações
    #cltd_aux=namevar.columns.values.tolist()
    #cltd_aux.remove("namespace")
    filtro_var=namevar
    filtro_var=pd.merge(filtro_var, ns_quartil, on=["namespace"], how='outer')

    # Ordenando Df

    filtro_var['ordem']=0
    for i in range(len(filtro_var['Risco'])):
        b=0
        a=filtro_var['Risco'][i]
        if a =='Alto Risco':
            b=int(1)
        elif a =='Risco':
            b=int(2)
        elif a =='Neutro':
            b=int(3)
        elif a =='Bom uso':
            b=int(4)
        filtro_var.loc[i,"ordem"]=b
    filtro_var=filtro_var.sort_values(by="ordem", ascending=True).reset_index(drop=True)
    filtro_var=reorder_columns(filtro_var, 'Risco',1)
    filtro_var=filtro_var.drop(['ordem'], axis=1).reset_index(drop=True)


    ######## Tabela quest

    filtro_ques=nameques
    filtro_ques=pd.merge(filtro_ques, ns_quartil, on=["namespace"], how='outer')

    # Ordenando Df

    filtro_ques['ordem']=0
    for i in range(len(filtro_ques['Risco'])):
        b=0
        a=filtro_ques['Risco'][i]
        if a =='Alto Risco':
            b=int(1)
        elif a =='Risco':
            b=int(2)
        elif a =='Neutro':
            b=int(3)
        elif a =='Bom uso':
            b=int(4)
        filtro_ques.loc[i,"ordem"]=b
    filtro_ques=filtro_ques.sort_values(by="ordem", ascending=True).reset_index(drop=True)
    filtro_ques=reorder_columns(filtro_ques, 'Risco',1)
    filtro_ques=filtro_ques.drop(['ordem'], axis=1).reset_index(drop=True)



    ######## Tabela rela

    filtro_rela=namerela
    filtro_rela=pd.merge(filtro_rela, ns_quartil, on=["namespace"], how='outer')

    # Ordenando Df

    filtro_rela['ordem']=0
    for i in range(len(filtro_rela['Risco'])):
        b=0
        a=filtro_rela['Risco'][i]
        if a =='Alto Risco':
            b=int(1)
        elif a =='Risco':
            b=int(2)
        elif a =='Neutro':
            b=int(3)
        elif a =='Bom uso':
            b=int(4)
        filtro_rela.loc[i,"ordem"]=b
    filtro_rela=filtro_rela.sort_values(by="ordem", ascending=True).reset_index(drop=True)
    filtro_rela=reorder_columns(filtro_rela, 'Risco',1)
    filtro_rela=filtro_rela.drop(['ordem'], axis=1).reset_index(drop=True)



'Aguarde só um momentinho'
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Processando {i+1}')
  bar.progress(i + 1)
  time.sleep(0.03)
'...pronto!'

if aux_filtro_show == 1:
    """

    """
    ans=name_quartil.copy()
    ans=ans[(ans["namespace"]==select)].reset_index(drop=True)
    ans=ans.loc[0,"Risco"]
    if ans == 'Alto Risco':
        st.write('### O Grau de Risco do namespace é: ',ans," 🔥")
    elif ans == 'Risco':
        st.write('### O Grau de Risco do namespace é: ',ans," ⚠️")
    elif ans == 'Neutro':
        st.write('### O Grau de Risco do namespace é: ',ans," 🥈")
    elif ans == 'Bom uso':
        st.write('### O Grau de Risco do namespace é: ',ans," 🥇")



    """

    """
    """

    """
    st.plotly_chart(figvar)
    st.plotly_chart(figques)
    st.plotly_chart(figrel)
else:
    ### Tabela variações
    st.write('Média (Sc-Eduqo) das métricas na tabela de variações')

    #Média Eduqo
    #arrumando média..
    lm=l_media_var.copy()
    alm=l_media_var.columns.values.tolist()
    #alm.remove("namespace")
    il=0
    lmedia=pd.DataFrame()

    for col in alm:
        listmaux=list()
        asx=lm.loc[il,col]
        axx=str(asx)+'%'
        listmaux.append(axx)
        za=pd.DataFrame(listmaux)
        lmedia[col]=za.sum()
    lmedia["namespace"]='Media SC-Eduqo'
    lmedia
    st.write('### Métricas na Tabela de Variação')

    """

    """
    # Arrumando Dataframe...
    aux_dict_var=filtro_var.columns.values.tolist()
    aux_dict_var.remove("namespace")
    if a_dict==1:
        aux_dict_var.remove("Risco")

    dict_var={col :"{:,.2f}%" for col in aux_dict_var}
    var_col_mask = filtro_var.dtypes.apply(lambda d: issubclass(np.dtype(d).type, np.number))
    filtro_var = filtro_var.style.format(dict_var).background_gradient(cmap='Greens')\
                                                        .set_properties(subset=filtro_var.columns[~var_col_mask], # right-align the numeric columns and set their width
                                                        **{'width':'10em', 'text-align':'left'})\
                                                        #.set_properties(subset=beneficios_grupo_total4.columns[numeric_col_mask], # right-align the numeric columns and set their width
                                                        #**{'width':'10em', 'text-align':'center'})

    #mostrando tabela
    st.dataframe(filtro_var)





    ### Tabela Questões
    st.write('Média (Sc-Eduqo) das métricas na tabela de questões')
    #Média Eduqo

    #arrumando média..
    lmq=l_media_ques.copy()
    almq=l_media_ques.columns.values.tolist()
    almq.remove("namespace")
    il=0
    lmediaq=pd.DataFrame()

    for col in almq:
        listmauxq=list()
        asxq=lmq.loc[il,col]
        axxq="{0:.2f}".format(asxq)
        listmauxq.append(axxq)
        zaq=pd.DataFrame(listmauxq)
        lmediaq[col]=zaq.sum()
    lmediaq["namespace"]='Media SC-Eduqo'
    lmediaq=reorder_columns(lmediaq,"namespace",0)
    lmediaq
    st.write('### Métricas na Tabela de Questões')
    """

    """
    # Arrumando Dataframe...
    aux_dict_ques=filtro_ques.columns.values.tolist()
    aux_dict_ques.remove("namespace")
    if a_dict==1:
        aux_dict_ques.remove("Risco")

    dict_ques={col :"{:,.2f}" for col in aux_dict_ques}
    ques_col_mask = filtro_ques.dtypes.apply(lambda d: issubclass(np.dtype(d).type, np.number))
    filtro_ques = filtro_ques.style.format(dict_ques).background_gradient(cmap='Greens')\
                                                        .set_properties(subset=filtro_ques.columns[~ques_col_mask], # right-align the numeric columns and set their width
                                                        **{'width':'10em', 'text-align':'left'})\


    #mostrando tabela
    st.dataframe(filtro_ques)


    ### Tabela rela

    st.write('Média (Sc-Eduqo) das métricas na tabela de relátorios')
    #Média Eduqo

    #arrumando média..
    lmr=l_media_relaa2.copy()
    almr=l_media_relaa2.columns.values.tolist()
    almr.remove("namespace")
    il=0
    lmediar=pd.DataFrame()

    for col in almr:
        listmauxr=list()
        asxr=lmr.loc[il,col]
        axxr="{0:.2f}".format(asxr)
        listmauxr.append(axxr)
        zar=pd.DataFrame(listmauxr)
        lmediar[col]=zar.sum()
    lmediar["namespace"]='Media SC-Eduqo'
    lmediar=reorder_columns(lmediar,"namespace",0)
    lmediar

    st.write('### Métricas na Tabela de Relátorios')
    """

    """
    # Arrumando Dataframe...
    aux_dict_rel=filtro_rela.columns.values.tolist()
    aux_dict_rel.remove("namespace")
    if a_dict==1:
        aux_dict_rel.remove("Risco")

    dict_rel={col :"{:,.2f}" for col in aux_dict_rel}
    rel_col_mask = filtro_rela.dtypes.apply(lambda d: issubclass(np.dtype(d).type, np.number))
    filtro_rela = filtro_rela.style.format(dict_rel).background_gradient(cmap='Greens')\
                                                        .set_properties(subset=filtro_rela.columns[~rel_col_mask], # right-align the numeric columns and set their width
                                                        **{'width':'10em', 'text-align':'left'})\


    #mostrando tabela
    st.dataframe(filtro_rela)

####################################### INSIGHTS ##############################

"""
### 💎 Iluminações ( Insights )
O foco ( por enquanto ) será em cima do mal uso da plataforma.
"""

expander_var = st.expander("Métricas de Variações -> (clique aqui 🖱️)")
expander_var.write("(1) Escolas com quedas drásticas no número de alunos interagindo, pode ser algo de grande risco, porque mostra que a escola ou perdeu alunos, ou não está realizando boa parte de suas rotinas na plataforma. (2) Variações grandes na parte de subida de conteúdos e interações dos alunos podem indicar, que a escola não estão realizando toda sua rotina conosco ( então estão realizando onde? pode ser uma solução da concorrência? ) indicando uma queda no valor enchergado na plataforma.")
expander_que = st.expander("Métricas de Questões -> (clique aqui 🖱️)")
expander_que.write("(1) Escolas que utilizam pouco o banco não valorizam um de nossos principais diferenciais competitivos em relação ao Google Classroom, então pode ser uma questão perigosa para potenciais churns. (2) Baixo uso de questões discursivas pode significar uma baixa personalização do uso da plataforma.")
expander_rel = st.expander("Métricas de Relátorios -> (clique aqui 🖱️)")
expander_rel.write("(1) Visualização de relatórios: Os nossos relatórios são um de nossos diferenciais para os concorrentes, e sua subutilização também pode indicar um mal uso da plataforma.")

####################################### Próximos Passos ##############################

"""
### 🛠️ Próximos Passos
(1) - Testar modelo para todas as escolas do Sucesso do Cliente.
"""
"""
(2) - Colocar novas métricas/tabelas recolhidas na pesquisa no modelo e avaliar se faz sentido ou não.
"""
"""
(3) - Automatização da geração de csv's para o GitHub
"""
"""
(4) - Estatística e Machine Learning para avaliar as correlações entre as váriaveis.
"""
