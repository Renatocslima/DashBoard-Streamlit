import pandas as pd
import numpy as np
from glob import glob
import streamlit as st
import plotly.express as px
import plotly.io as pio


@st.cache_data
def load_and_concatenate_data(file_pattern='datasets/*.csv', sep=';'):
    # Encontrar arquivos correspondentes ao padrão
    files = glob(file_pattern)
    if not files:
        raise ValueError(f"No files found for the pattern {file_pattern}")
    
    # Carregar e concatenar os arquivos
    dataframes = [pd.read_csv(file, sep=sep, low_memory=False) for file in files]
    return pd.concat(dataframes, ignore_index=True)

@st.cache_data
def preprocess_data(df):
    df['Agente do Cadastro'] = df['Agente do Cadastro'].replace(0, 'Vazio')
    df['Agente do Cadastro'] = df['Agente do Cadastro'].fillna('Vazio')
    df['Agente do Cadastro'] = df['Agente do Cadastro'].astype(str)
    df['Tipo de Validação'] = df['Tipo de Validação'].fillna('Não Validado')
    df['Tipo de Validação'] = df['Tipo de Validação'].replace(' ', 'Não Validado')
    df['Data da Validação'] = df['Data da Validação'].fillna("01/01/1900 00:00:00")
    df = df.fillna(0)
    df['Data do Cadastro'] = pd.to_datetime(df['Data do Cadastro'], dayfirst=True, format='mixed')
    df['Data da Validação'] = pd.to_datetime(df['Data da Validação'], dayfirst=True, format='mixed')
    df['dt_validação'] = df['Data da Validação'].dt.date
    df = df.sort_values(['Data da Validação'], ascending=False)
    df = df.sort_values(['Data do Cadastro'], ascending=False)
    df['Year'] = df['Data do Cadastro'].dt.year.astype(str)
    df['Month'] = df['Data do Cadastro'].dt.month.astype(str)
    df['Day'] = df['Data do Cadastro'].dt.strftime('%d')
    df['Hour'] = df['Data do Cadastro'].dt.strftime('%H')
    df['Ano de Validação'] = df['Data da Validação'].dt.year.astype(str)
    df['Mês de Validação'] = df['Data da Validação'].dt.month.astype(str)
    nao_validavel = ['MORADOR IMPEDIU', 'CASA FECHADA 1ª VISITA', 'CASA FECHADA 2ª VISITA', 'Casa Fechada', 'Morador impediu']
    df['Tipo de Ocorrência'] = df['Ocorrências'].apply(lambda x: 'Não validável' if x in nao_validavel else 'Validável')
    return df

@st.cache_data
def create_bar_chart(data, x, y, color, title, orientation='v', color_map=None, color_map1=None, text_auto=True):
    fig = px.bar(data, x=x, y=y, color=color, title=title, text_auto=text_auto, color_discrete_map=color_map, color_discrete_sequence=color_map1, orientation=orientation)
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
    fig = px.line(data, x=x, y=y, color=color, title=title, color_discrete_map=color_map, color_discrete_sequence=color_map1, markers=True, text=y, line_shape='spline')
    fig.update_layout(legend=dict(
        orientation='h',
        xanchor='center',
        yanchor='bottom',
        x=0.5,
        y=-0.5
    ))
    fig.update_layout(
    xaxis=dict(
        tickmode='linear',
        tickangle=0  # Ajusta o ângulo dos rótulos para melhorar a legibilidade
    ))
    return fig

