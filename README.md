# Streamlit - Código para Apresentação de Dashboards

## 🚀 Sobre o Projeto

Este projeto apresenta um exemplo de como construir dashboards interativos utilizando [Streamlit](https://streamlit.io/). O objetivo é carregar dados a partir de arquivos CSV armazenados na pasta `datasets`, processá-los e gerar visualizações interativas. O projeto é dividido em várias páginas, cada uma com uma funcionalidade específica.

## 📂 Estrutura do Projeto

- **datasets/**: Pasta onde os arquivos CSV devem ser armazenados. O aplicativo carrega todos os arquivos desta pasta automaticamente.
- **1_home.py**: Arquivo principal do Streamlit que executa o dashboard inicial.
- **pages/**: Contém as páginas adicionais do dashboard.
  - **2_page2.py**: Segunda página do dashboard, com funcionalidades adicionais.
  - **3_page3.py**: Terceira página do dashboard, com mais visualizações ou análises.
- **utils/data_utils.py**: Funções auxiliares para carregar, preprocessar e visualizar os dados.
- **README.md**: Este arquivo, com instruções para configuração e execução do projeto.

## 🛠️ Funcionalidades

- **Carregamento de Dados**: Carrega automaticamente todos os arquivos CSV da pasta `datasets`.
- **Pré-processamento**: Limpeza e transformação dos dados para facilitar a análise.
- **Visualizações Interativas**: Gráficos interativos gerados com Plotly para análise de dados.
- **Navegação por Múltiplas Páginas**: O dashboard é dividido em várias páginas, cada uma focada em diferentes aspectos dos dados.

## 📋 Preparando o Ambiente

### 1. Criar um ambiente virtual

Recomenda-se o uso de um ambiente virtual para isolar as dependências do projeto:

```bash
python -m venv .venv
```

### 2. Ativar o ambiente virtual

- **Windows**:
  ```bash
  .venv\Scripts\activate.bat
  ```
- **macOS/Linux**:
  ```bash
  source .venv/bin/activate
  ```

### 3. Instalar as dependências

Após ativar o ambiente virtual, instale o Streamlit e outras dependências do projeto:

```bash
pip install -r requirements.txt
```

### 4. Testar a instalação

Para garantir que tudo está instalado corretamente, execute:

```bash
streamlit hello
```

### 5. Executar o Dashboard

Com o ambiente configurado e as dependências instaladas, execute o aplicativo:

```bash
streamlit run 1_home.py
```

O comando acima abrirá o dashboard no navegador. O aplicativo carregará automaticamente os arquivos CSV da pasta `datasets`, processará os dados e exibirá as visualizações correspondentes.

## 📊 Como Funciona

1. **Carregar dados**: O aplicativo utiliza a função `load_and_concatenate_data()` para carregar todos os arquivos CSV encontrados na pasta `datasets`.

2. **Pré-processar dados**: Os dados carregados são processados pela função `preprocess_data()` que realiza a limpeza e formatação necessária.

3. **Visualizar dados**: Após o pré-processamento, diferentes gráficos e tabelas são gerados automaticamente para facilitar a análise dos dados.

4. **Navegação por Páginas**: O dashboard está dividido em múltiplas páginas (`1_home.py`, `2_page2.py`, `3_page3.py`), permitindo que o usuário explore diferentes análises e visualizações.

## 📝 Exemplos de Uso

- **Análise de Dados de Vendas**: Coloque seus dados de vendas na pasta `datasets` e veja gráficos e tabelas que resumem as vendas por período, categoria, etc.
- **Monitoramento de KPIs**: Use o dashboard para monitorar indicadores-chave de performance (KPIs) inserindo os dados na pasta correta.

## 🌐 Mais Informações

Para mais informações sobre a instalação e uso do Streamlit, consulte a [documentação oficial](https://docs.streamlit.io/get-started/installation).

## 🤝 Contribuição

Contribuições são bem-vindas! Se você tiver sugestões ou encontrar algum bug, sinta-se à vontade para abrir uma issue ou enviar um pull request.

### Como Contribuir

1. **Fork o projeto**
2. **Crie uma branch para sua feature** (`git checkout -b feature/NomeDaFeature`)
3. **Commit suas mudanças** (`git commit -m 'Adiciona nova feature'`)
4. **Dê um push na sua branch** (`git push origin feature/NomeDaFeature`)
5. **Abra um Pull Request**

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🎓 Referências

- [Documentação do Streamlit](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)

## ✨ Agradecimentos

Agradecimentos a todos que contribuíram direta ou indiretamente para este projeto.