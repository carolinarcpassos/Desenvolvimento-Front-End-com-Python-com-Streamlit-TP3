# 📊 Dashboard Analítico de Turismo do Rio de Janeiro (Data.Rio)

Este repositório contém o desenvolvimento de uma aplicação web interativa em **Streamlit** focada na análise exploratória de dados de turismo da cidade do Rio de Janeiro. O projeto foi construído de forma incremental e modular, aplicando diversas bibliotecas do ecossistema de Ciência de Dados em Python para enriquecer as visualizações e análises teóricas.

---

## 📂 Estrutura do Projeto

├── app_tp3_carolina_ramos_da_costa_passos.py                   # Código-fonte principal com os 12 exercícios implementados
├── .gitignore                                                  # Configuração para ignorar arquivos de sistema e ambientes virtuais (.venv/)
├── requirements.txt                                            # Bibliotecas e dependências do projeto para replicação do ambiente
└── README.md                                                   # Documentação do projeto (este arquivo)

---

## 📥 Fonte dos Dados (Data.Rio)

O arquivo de dados utilizado na aplicação foi obtido diretamente do portal oficial Data.Rio:

* **Tabela Utilizada**: Tabela 2674 - Chegada de turistas ao Rio de Janeiro por via de acesso (2006-2019)
* **Formato do Arquivo**: Arquivo em formato Excel (.xls)
* **Conteúdo**: Dados históricos anuais discriminados por país de origem e modais de transporte receptivo (via aérea e via marítima).
* **Link de acesso**: https://www.data.rio/documents/665ce86a7a2e4c0fa523b7b7636513e0/about

---

🚀 Como Executar o Projeto Localmente (Linux Mint / Ubuntu)
Siga os passos abaixo no terminal do seu sistema para configurar o ambiente e rodar o aplicativo:

1. Clonar o Repositório
git clone https://github.com/carolinarcpassos/Desenvolvimento-Front-End-com-Python-com-Streamlit-TP3.git
cd Desenvolvimento-Front-End-com-Python-com-Streamlit-TP3

2. Criar e Ativar o Ambiente Virtual
python3 -m venv .venv
source .venv/bin/activate

3. Instalar as Dependências
pip install --upgrade pip
pip install -r requirements.txt

4. Executar o Dashboard
streamlit run app_tp3_carolina_ramos_da_costa_passos.py
A aplicação abrirá automaticamente no seu navegador padrão em http://localhost:8501.

---

🎯 Exercícios Implementados no Dashboard

Exercício 1: Escolha dos Datasets e Explicação do Objetivo e Motivação
Prático: 
Apresentação detalhada da escolha do dataset da Tabela 2674 (Chegada de turistas ao Rio de Janeiro por via de acesso), explicando a motivação estratégica de mapear o fluxo receptivo internacional e detalhando as funcionalidades e visualizações desenvolvidas no painel.

Exercício 2: Realizar Upload de Arquivo XLS
Prático: 
Construção da interface em Streamlit utilizando st.file_uploader para permitir ao usuário carregar arquivos XLS nativos do portal Data.Rio.

Exercício 3: Filtro de Dados e Seleção
Prático: 
Implementação de três seletores interativos distintos na interface (radio button para vias de acesso, selectbox para ano de destaque e checkbox com dropdown para seleção por país), permitindo o filtro completo de linhas e colunas.

Exercício 4: Criar Visualizações de Dados - Tabelas
Prático: 
Exibição dos dados filtrados através de uma tabela interativa com st.dataframe que reage instantaneamente aos seletores do usuário e permite a ordenação e filtragem direta das colunas.

Exercício 5: Desenvolver Serviço de Download de Arquivos
Prático: 
Implementação de serviço de exportação de dados com st.download_button, permitindo ao usuário baixar a tabela filtrada diretamente no formato Excel (.xlsx).

Exercício 6: Utilizar Barra de Progresso e Spinners
Prático: 
Adição de barra de progresso (st.progress) e spinner (st.spinner) para fornecer feedback visual ao usuário sobre o processamento e a sanitização do arquivo XLS.

Exercício 7: Utilizar Color Picker
Prático: 
Inclusão do componente st.color_picker na barra lateral para permitir a personalização em tempo real da cor de fundo da aplicação e das fontes do painel via CSS dinâmico.

Exercício 8: Utilizar Funcionalidade de Cache
Prático: 
Aplicação da funcionalidade de cache do Streamlit (@st.cache_data) no carregamento e parsing dos arquivos XLS para evitar reprocessamentos desnecessários a cada interação na tela.

Exercício 9: Persistir Dados Usando Session State
Prático: 
Implementação do st.session_state para manter as preferências de estilo e personalização visual escolhidas pelo usuário durante toda a navegação na aplicação.

Exercício 10: Criar Visualizações de Dados - Gráficos Simples
Prático: 
Desenvolvimento de gráficos simples e interativos (barras para os top países, linhas para a evolução histórica e pizza para a proporção entre países) utilizando Plotly Express.

Exercício 11: Criar Visualizações de Dados - Gráficos Avançados
Prático: 
Criação de gráficos avançados para análises aprofundadas, incluindo um histograma da distribuição do fluxo de turistas e um scatter plot para correlacionar o modal aéreo em relação ao marítimo.

Exercício 12: Exibir Métricas Básicas
Prático: 
Construção de cartões de métricas (st.metric) exibindo resumos estatísticos rápidos, como contagem de países, somatórios por modal e médias ajustadas dinamicamente segundo os filtros selecionados.


👤 Carolina Passos - Git: carolinarcpassos/Desenvolvimento-Front-End-com-Python-com-Streamlit-TP3