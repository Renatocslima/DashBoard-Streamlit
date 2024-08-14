import pandas as pd
from glob import glob
import plotly.express as px
import streamlit as st

@st.cache_data
def load_and_concatenate_data(file_pattern='datasets/*.csv', sep=';'):
    """
    Carrega múltiplos arquivos CSV que correspondem ao padrão de arquivo fornecido e os concatena em um único DataFrame.

    Parâmetros:
    file_pattern (str): O padrão dos arquivos a serem lidos. Default é 'datasets/*.csv'.
    sep (str): O separador usado nos arquivos CSV. Default é ';'.

    Retorna:
    pd.DataFrame: Um DataFrame contendo os dados concatenados de todos os arquivos correspondentes.

    Lança:
    ValueError: Se nenhum arquivo for encontrado com o padrão especificado.
    """
    # Encontrar arquivos correspondentes ao padrão
    files = glob(file_pattern)
    if not files:
        raise ValueError(f"No files found for the pattern {file_pattern}")
    
    # Carregar e concatenar os arquivos
    dataframes = [pd.read_csv(file, sep=sep, low_memory=False) for file in files]
    return pd.concat(dataframes, ignore_index=True)

@st.cache_data
def preprocess_data(df):
    """
    Realiza o pré-processamento do DataFrame fornecido, incluindo a exclusão de colunas, substituição de valores, 
    conversão de tipos de dados e criação de colunas condicionais.

    Parâmetros:
    df (pd.DataFrame): O DataFrame a ser pré-processado.

    Retorna:
    pd.DataFrame: O DataFrame pré-processado.
    """
    # Excluir colunas desnecessárias do df
    excluir_colunas = ['']  # Especifique as colunas a serem excluídas
    df.drop(excluir_colunas, axis=1, errors='ignore', inplace=True)
    
    # Substituir valores em uma coluna específica
    df['Coluna'] = df['Coluna'].replace('Valor a ser alterado', 'Novo Valor')
    df['Coluna'] = df['Coluna'].fillna('Valor a ser colocado em células vazias')
    
    # Preencher valores NaN em todo o DataFrame com 0
    df = df.fillna(0)
    
    # Definir tipos de coluna
    df['Coluna_texto'] = df['Coluna_texto'].astype(str)  # Como String
    df['Coluna_data'] = pd.to_datetime(df['Coluna_data'], dayfirst=True, format='mixed')  # Como DataTime
    df['Coluna_data'] = df['Coluna_data'].dt.date  # Como Data (removendo a hora)
    
    # Classificar o DataFrame por uma coluna de data em ordem decrescente
    df = df.sort_values(['Coluna_data'], ascending=False) 
    
    # Extração de partes da data para novas colunas
    df['Year'] = df['Coluna_data'].apply(lambda x: x.year).astype(str)
    df['Month'] = df['Coluna_data'].apply(lambda x: x.month).astype(str)
    df['Day'] = df['Coluna_data'].apply(lambda x: x.strftime('%d'))
    df['Hour'] = df['Coluna_data'].apply(lambda x: x.strftime('%H'))
    
    # Criação de colunas condicionais
    condição = ['Lista de itens da condição']
    df['Coluna Condicional'] = df['Coluna'].apply(lambda x: 'Condição verdadeira' if x in condição else 'Condição falsa')

    return df

@st.cache_data
def create_bar_chart(data, x, y, color, title, orientation='v', color_map=None, color_map1=None, text_auto=True):
    """
    Cria um gráfico de barras usando o Plotly Express.

    Parâmetros:
    data (pd.DataFrame): O DataFrame contendo os dados.
    x (str): O nome da coluna para o eixo X.
    y (str): O nome da coluna para o eixo Y.
    color (str): O nome da coluna para a cor das barras.
    title (str): O título do gráfico.
    orientation (str): A orientação das barras ('v' para vertical, 'h' para horizontal). Default é 'v'.
    color_map (dict): Um mapeamento opcional de cores específicas.
    color_map1 (list): Uma sequência opcional de cores para usar.
    text_auto (bool): Se True, exibe os valores das barras automaticamente. Default é True.

    Retorna:
    plotly.graph_objs._figure.Figure: A figura do gráfico de barras.
    """
    fig = px.bar(
        data, x=x, y=y, color=color, title=title, text_auto=text_auto, 
        color_discrete_map=color_map, color_discrete_sequence=color_map1, 
        orientation=orientation
    )
    
    # Configuração da legenda
    fig.update_layout(legend=dict(
        orientation='h',
        xanchor='center',
        yanchor='bottom',
        x=0.5,
        y=-0.5
    ))
    
    return fig

@st.cache_data
def create_line_chart(data, x, y, color, title, color_map=None, color_map1=None):
    """
    Cria um gráfico de linhas usando o Plotly Express.

    Parâmetros:
    data (pd.DataFrame): O DataFrame contendo os dados.
    x (str): O nome da coluna para o eixo X.
    y (str): O nome da coluna para o eixo Y.
    color (str): O nome da coluna para a cor das linhas.
    title (str): O título do gráfico.
    color_map (dict): Um mapeamento opcional de cores específicas.
    color_map1 (list): Uma sequência opcional de cores para usar.

    Retorna:
    plotly.graph_objs._figure.Figure: A figura do gráfico de linhas.
    """
    fig = px.line(
        data, x=x, y=y, color=color, title=title, color_discrete_map=color_map, 
        color_discrete_sequence=color_map1, markers=True, text=y, line_shape='spline'
    )
    
    # Configuração da legenda
    fig.update_layout(legend=dict(
        orientation='h',
        xanchor='center',
        yanchor='bottom',
        x=0.5,
        y=-0.5
    ))
    
    # Configuração dos rótulos do eixo X
    fig.update_layout(
        xaxis=dict(
            tickmode='linear',
            tickangle=0  # Ajusta o ângulo dos rótulos para melhorar a legibilidade
        )
    )
    
    return fig

@st.cache_data
def create_pie_chart(data, x, y, title):
    """
    Cria um gráfico de pizza usando o Plotly Express.

    Parâmetros:
    data (pd.DataFrame): O DataFrame contendo os dados.
    x (str): O nome da coluna para os rótulos das fatias.
    y (str): O nome da coluna para os valores das fatias.
    title (str): O título do gráfico.

    Retorna:
    plotly.graph_objs._figure.Figure: A figura do gráfico de pizza.
    """
    fig = px.pie(data, names=x, values=y, title=title)
    
    # Configuração da legenda
    fig.update_layout(legend=dict(
        orientation='v',
        xanchor='left',
        yanchor='top',
        x=0.5,
        y=0
    ))
    
    return fig

@st.cache_data
def create_pivot_table(data, values, index, col, func, fill=None):
    """
    Cria uma tabela dinâmica (pivot table) a partir de um DataFrame.

    Parâmetros:
    data (pd.DataFrame): O DataFrame contendo os dados.
    values (str): O nome da coluna para os valores da tabela.
    index (str): O nome da coluna para o índice da tabela.
    col (str): O nome da coluna para as colunas da tabela.
    func (str or func): A função de agregação (ex: 'sum', 'mean', etc.).
    fill (scalar, optional): Valor a ser usado para preencher células vazias.

    Retorna:
    pd.DataFrame: O DataFrame resultante da tabela dinâmica, com colunas adicionais para Total e Média.
    """
    # Criação da tabela dinâmica (pivot table)
    pivot = pd.pivot_table(
        data=data, values=values, index=index, columns=col, 
        aggfunc=func, fill_value=fill
    )
    
    # Adiciona uma coluna 'Total' com a soma dos valores por linha
    pivot['Total'] = pivot.sum(axis=1)
    
    # Calcula a média dos valores (excluindo a coluna 'Total') e adiciona como uma nova coluna
    media_valores = pivot.drop(columns=['Total']).mean(axis=1)
    media_valores = media_valores.round(0).astype(int)
    pivot['Média'] = media_valores
    
    return pivot
