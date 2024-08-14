import streamlit as st
import pandas as pd
from utils.data_utils import load_and_concatenate_data, preprocess_data, create_bar_chart, create_pie_chart, create_line_chart, create_pivot_table

# - Configuração da Página
st.set_page_config(layout="wide")

def main():
    st.title("Dashboard")
    st.write("")

    # Apenas para teste
    # -------------------------------------------------
    col01, col02 = st.columns(2)
    nome = col01.text_input("Qual seu nome?")
    num_linhas = col02.number_input("Digite um número de 0 a 9", min_value=0, max_value=9, step=1)
    st.markdown(f"<h3 style='font-size:18px;'> Olá {nome}, esse é um Dashboard exemplo no Streamlit, edite para pegar seus dados e criar as tabelas e os gráficos que precisa.</h3>", unsafe_allow_html=True)
    numeros = list(range(0, num_linhas + 1))
    
    df=pd.DataFrame({
    'coluna': numeros,
    'numeros': numeros})

    df['tipo'] = df['numeros'].apply(lambda x: 'Par' if x % 2 == 0 else 'Ímpar')
    # -------------------------------------------------

    # Esse código carrega e trata seus arquivos .csv presentes na pasta datasets de acordo com data_utils.py, retire o simbolo de comentário
    # -------------------------------------------------
    # - Carregar dados
    #df = load_and_concatenate_data()

    # - Pré-processar dados
    #df = preprocess_data(df)
    # -------------------------------------------------

    col11, col12 = st.columns(2)
    col21, col22 = st.columns(2)
    col31, col32 = st.columns(2)

    # - Configuração de Filtro
    st.sidebar.header("Titulo do Sidebar")
    lista_de_seleção = ['Todos'] + list(df['tipo'].unique())
    seleção = st.sidebar.selectbox('Titulo do Filtro', lista_de_seleção)
    
    if seleção == 'Todos': filtro = lista_de_seleção
    else: filtro = [seleção]

    df_filtrado = df[df['tipo'].isin(filtro)]

    # - Gráficos
    color_map = {'Item1': '#00049E', 'Item2': '#7275FE', 'Item3': 'gray'}
    color_map1 = ['#00049E','#7275FE']

    tabela = df_filtrado.groupby(['coluna', 'tipo'])['numeros'].sum().reset_index()#.count().reset_index()

    tabela=tabela.sort_values(by=['numeros'], ignore_index=True)
    col11.write("Tabela Agrupada")
    col11.table(tabela)

    pivot = create_pivot_table(df_filtrado, values='numeros', index=['tipo'], col='coluna', func='sum', fill=0)
    col12.write("Tabela Dinâmica")
    col12.table(pivot)

    fig_bar = create_bar_chart(tabela, x='coluna', y='numeros', color='tipo', title="Titulo do Gráfico")
    col21.plotly_chart(fig_bar)

    fig_pie = create_pie_chart(tabela, x='coluna', y='numeros', title="Titulo do Gráfico")
    col22.plotly_chart(fig_pie)

    fig_line = create_line_chart(tabela, x='coluna', y='numeros', color=None, title="Titulo do Gráfico", color_map=color_map)
    col31.plotly_chart(fig_line)

    fig_bar_h = create_bar_chart(tabela, y='coluna', x='numeros', title="Titulo do Gráfico", orientation='h')
    col32.plotly_chart(fig_bar_h)

if __name__ == "__main__":
    main()
