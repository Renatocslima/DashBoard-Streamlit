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
    excluir_colunas = ['Setor', 'Quadra', 'Lote', 'Sublote', 'Endereço Referência Antes', 
                  'Nr. Imóvel Antes', 'Endereço Referência Depois', 'Nr. Imóvel Depois', 
                  'Bairro', 'Logradouro', 'Complemento', 'CEP Antes', 'CEP Depois', 'Controlador', 
                  'Id do Controlador', 'Data Inclusão do Controlador', 'Entrevistado', 'Tipo do Entrevistado', 
                  'Qualidade da Água', 'Regularidade do Fornecimento', 'Tipo de Pessoa Antes', 'Tipo de Pessoa Depois', 
                  'Nome do Consumidor Antes', 'Nome do Consumidor Depois', 'CPF/CNPJ Antes', 'CPF/CNPJ Depois', 'Nr. RG Antes', 
                  'Nr. RG Depois', 'Dt. Emissão do RG Antes', 'Dt. Emissão do RG Depois', 'Orgão Expedidor RG Antes', 
                  'Orgão Expedidor RG Depois', 'UF Antes', 'UF Depois', 'Data Nasc. Antes', 'Data Nasc. Depois', 
                  'Autorização de Envio de Campanhas', 'E-mail Antes', 'E-mail Depois', 'Telefones Fixos Antes', 
                  'Telefones Fixos Depois', 'Telefones Móveis Antes', 'Telefones Móveis Depois', 'Perfil do Imóvel', 
                  'Analisar Tarifa Social', 'Nr. Celpe', 'Pav. Rua Antes', 'Pav. Rua Depois', 'Pav. Calçada Antes', 
                  'Pav. Calçada Depois', 'Fonte de Abastecimento Antes', 'Fonte de Abastecimento Depois', 'Possui Fossa?', 
                  'Possui Piscina Antes?', 'Possui Piscina Depois?', 'Volume Piscina', 'Possui Cisterna?', 'Possui Caixa de Inspeção?', 
                  'Teste de Cloro', 'Teste de Torneira Ligada', 'Sit. Imóvel', 'Matr. Vizinho', 'Matr. Unificado', 'Sit. Água Antes', 
                  'Sit. Água Depois', 'Sit. Esgoto Antes', 'Sit. Esgoto Depois', 'Tipo Esgotamento Antes', 'Tipo Esgotamento Depois', 
                  'Nr. Hd Antes', 'Nr. Hd Depois', 'Local de Instalação Antes', 'Local de Instalação Depois', 'Proteção Hd Antes', 
                  'Proteção Hd Depois', 'Possui Cavalete Antes?', 'Possui Cavalete Depois?', 'Leitura Antes', 'Leitura Depois', 
                  'Condições do HD', 'Condições do Abrigo do HD', 'Fontes Alternativas Antes', 'Fontes Alternativas Depois', 
                  'Nr. Moradores Antes', 'Nr. Moradores Depois', 'Acessório de Rede Esgoto', 'Local Acessório de Rede Esgoto', 
                  'Suspeita de Irregularidades', 'Vazamento', 'Observações', 'Observações Internas', 'Foto da Fachada', 'Foto do Medidor', 
                  'Foto da Caixa de Inspeção', 'Foto da Fraude', 'Foto do Vazamento', 'Foto da Mudança de Titularidade', 
                  'Foto do Teste de Cloro', 'Foto Extra', 'Foto da Instalação', 'Foto do Formulário', 'Id do Agente do Cadastro', 
                  'Data de Inclusão do Agente do Cadastro', 'Número da Visita', 'Data Envio Fluir', 'Nome Arquivo Retorno Fluir', 
                  'Usuário da Exportação', 'Data Reenvio Fluir', 'Nome Arquivo Correção Fluir', 'Usuário da Exportação da Correção', 
                  'Nome do Arquivo SAN', 'Observação da Validação', 'Data da Auditoria', 'Auditor', 'Observação da Auditoria', 
                  'Tipo da Auditoria']
    df.drop(excluir_colunas, axis=1, errors='ignore', inplace=True)
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
    df['Ocorrências'] = df['Ocorrências'].str.upper()
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

