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
   
    col11, col12 = st.columns(2)
    col21, col22 = st.columns(2)
    col31, col32 = st.columns(2)
    
    # Configuração de Filtro
    local = ['TODAS'] + list(df['Localidade'].unique())
    localidade = st.sidebar.selectbox('Localidade', local)
    ano = st.sidebar.selectbox('Ano', df['Year'].unique())
    mes = st.sidebar.selectbox('Mês', df['Month'].unique())

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
    color_map = {'Validado': '#00049E', 'Não Validado': '#7275FE', 'Aguardando Análise': 'gray', 'Complemento de Fotos e Informações': 'gray', 'Revisão Interna': 'gray'}
    color_map1 = ['#00049E','#7275FE']

    prod_dia = df_filtrado.groupby(['Day', 'Tipo de Validação'])['Matrícula'].count().reset_index()
    fig_date = create_line_chart(prod_dia, 'Day', 'Matrícula', 'Tipo de Validação', "Visitas por dia", color_map=color_map)
    col11.plotly_chart(fig_date)

    Agente_dia = df_filtrado.groupby(df_filtrado['Day'])['Agente do Cadastro'].nunique().reset_index()
    fig_date = create_line_chart(Agente_dia, 'Day', 'Agente do Cadastro', None, "Visitas por dia", color_map1=color_map1)
    col11.plotly_chart(fig_date)

    #city_total = df_filtrado.groupby(['Localidade', 'Tipo de Validação'])['Matrícula'].count().reset_index()
    #fig_local = create_bar_chart(city_total, 'Localidade', 'Matrícula', 'Tipo de Validação', "Visitas por Localidade", color_map=color_map)
    #col12.plotly_chart(fig_local)

    #ocorrencia_total = df_filtrado.groupby('Ocorrências')['Matrícula'].count().reset_index().sort_values('Matrícula')
    #fig_ocorrencia = create_bar_chart(ocorrencia_total, 'Matrícula', 'Ocorrências', None, "Visitas por Ocorrência", orientation='h', color_map1=color_map1)
    #col31.plotly_chart(fig_ocorrencia)

    #fig_ocorrencia1 = px.pie(ocorrencia_total, names='Ocorrências', values='Matrícula', title="% Visitas por Ocorrência")
    #fig_ocorrencia1.update_layout(legend=dict(
    #    orientation='v',
    #    xanchor='left',
    #    yanchor='top',
    #    x=0.5,
    #    y=0
    #))
    #col32.plotly_chart(fig_ocorrencia1)

    #val_total = df_validação.groupby('Mês de Validação')['Matrícula'].count().reset_index()
    #fig_date_val = create_bar_chart(val_total, 'Mês de Validação', 'Matrícula', None, "Validação por Mês", color_map1=color_map1)
    #col21.plotly_chart(fig_date_val)

    #val_total1 = df_validação.groupby('Localidade')['Matrícula'].count().reset_index()
    #fig_local_val = create_bar_chart(val_total1, 'Localidade', 'Matrícula', None, "Validação por Localidade", color_map1=color_map1)
    #col22.plotly_chart(fig_local_val)

if __name__ == "__main__":
    main()

