import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_utils import load_and_concatenate_data, preprocess_data, create_bar_chart, create_line_chart

# Configuração da Página
st.set_page_config(layout="wide")

def main():
        
    st.title("Dashboard de Visitas por dia")

    # Carregar dados
    df = load_and_concatenate_data()

    # Pré-processar dados
    df = preprocess_data(df)
    
    # Configuração de Filtro
    l0 = list(df['Localidade'].unique())
    l0.sort()
    local = ['TODAS'] + l0
    m0 = list(df['Month'].unique())
    m0.sort(reverse=True)
    localidade = st.sidebar.selectbox('Localidade', local)
    ano = st.sidebar.selectbox('Ano', df['Year'].unique())
    mes = st.sidebar.selectbox('Mês', m0)

    if localidade == 'TODAS':
        filtro = local
    else:
        filtro = [localidade]

    df_filtrado = df[(df['Year'] == ano) & (df['Month'] == mes)]
    df_filtrado = df_filtrado[df_filtrado['Localidade'].isin(filtro)]
    df_filtrado = df_filtrado.sort_values(['Data do Cadastro'], ascending=False)

    df_validação = df[(df['Ano de Validação'] == ano) & (df['Month'] == mes) & (df['Tipo de Validação'] == 'Validado')]
    df_validação = df_validação[df_validação['Localidade'].isin(filtro)]

    # Gráficos
    color_map = {'Validado': '#00049E', 'Não Validado': '#7275FE', 'Aguardando Análise': 'gray', 
                 'Complemento de Fotos e Informações': 'gray', 'Revisão Interna': 'gray',
                 'Validável': '#00049E', 'Não Validável': 'gray'}
    color_map1 = ['#00049E','#7275FE']

    prod_dia = df_filtrado.groupby(['Day', 'Tipo de Ocorrência'])['Matrícula'].count().reset_index()
    fig_date = create_line_chart(prod_dia, 'Day', 'Matrícula', 'Tipo de Ocorrência', "Visitas por dia", color_map=color_map)
    st.plotly_chart(fig_date)

    Agente_dia = df_filtrado.groupby(df_filtrado['Day'])['Agente do Cadastro'].nunique().reset_index()
    fig_agente = create_line_chart(Agente_dia, 'Day', 'Agente do Cadastro', None, "N° de agentes por dia", color_map1=color_map1)
    st.plotly_chart(fig_agente)

    pivot_table = pd.pivot_table(df_filtrado, values='Matrícula', index=['Localidade','Agente do Cadastro'], columns='Day', aggfunc='count', fill_value=0)
    st.markdown("<h3 style='font-size:16px;'> Produção de Agentes por dia </h3>", unsafe_allow_html=True)
    st.dataframe(pivot_table)
    st.write("")

if __name__ == "__main__":
    main()

