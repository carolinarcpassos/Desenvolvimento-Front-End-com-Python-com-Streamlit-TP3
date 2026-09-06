import io
import time
import pandas as pd
import plotly.express as px
import streamlit as st

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Data.Rio - Turismo Rio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Termos regionais/totais que devem ser removidos para manter apenas países
CONTINENTES_E_TOTAIS = [
    "ÁFRICA",
    "AMÉRICA CENTRAL",
    "AMÉRICA DO NORTE",
    "AMÉRICA DO SUL",
    "ÁSIA",
    "EUROPA",
    "OCEANIA",
    "ORIENTE MÉDIO",
    "OUTROS",
    "TOTAL",
    "CONTINENTE",
]


# ==============================================================================
# Exercício 9. Persistir Dados Usando Session State:
# Implemente a persistência de dados na aplicação utilizando Session State para
# manter as preferências do usuário (seleções e filtros escolhidos) durante a navegação.
# ==============================================================================
if "bg_color" not in st.session_state:
    st.session_state["bg_color"] = "#0E1117"

if "text_color" not in st.session_state:
    st.session_state["text_color"] = "#FFFFFF"


# ==============================================================================
# Exercício 8. Utilizar Funcionalidade de Cache:
# Utilize a funcionalidade de cache do Streamlit para armazenar os dados carregados
# dos arquivos XLS, evitando a necessidade de recarregá-los a cada nova interação.
# ==============================================================================
@st.cache_data(ttl=600, show_spinner=False)
def carregar_e_limpar_dados(uploaded_file):
    xls = pd.ExcelFile(uploaded_file)
    all_records = []
    sheet_years = [s for s in xls.sheet_names if s.isdigit()]

    MAPEAMENTO_PAISES = {
        "ÍNDIA": "Índia",
        "REPÚBLICA DA COREIA": "República da Coreia",
        "REPÚBLICA DA CORÉIA": "República da Coreia",
        "COREIA": "República da Coreia",
        "COREIA DO SUL": "República da Coreia",
        "ESTADOS UNIDOS": "Estados Unidos",
        "ESTADOS UNIDOS DA AMÉRICA": "Estados Unidos",
    }

    for year_str in sheet_years:
        df_sheet = pd.read_excel(xls, sheet_name=year_str)
        for idx in range(7, len(df_sheet)):
            name = df_sheet.iloc[idx, 0]
            if pd.isna(name):
                continue

            name_str = str(name).strip()

            if (
                not name_str
                or name_str.startswith("Fonte")
                or name_str.startswith("Nota")
                or name_str.startswith("(")
                or name_str.startswith("-")
                or "Disponível em" in name_str
                or "http" in name_str
            ):
                continue

            total_val = df_sheet.iloc[idx, 1]
            aerea_val = df_sheet.iloc[idx, 2]
            maritima_val = (
                df_sheet.iloc[idx, 3] if df_sheet.shape[1] > 3 else 0
            )

            all_records.append(
                {
                    "Ano": int(year_str),
                    "Pais": name_str,
                    "Total": total_val,
                    "Aérea": aerea_val,
                    "Marítima": maritima_val,
                }
            )

    df = pd.DataFrame(all_records)

    for col in ["Total", "Aérea", "Marítima"]:
        df[col] = df[col].replace(["-", "...", " - ", "—"], 0)
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df["Pais"] = df["Pais"].str.title()

    df["Pais_Upper"] = df["Pais"].str.upper()
    for chave, valor_padrao in MAPEAMENTO_PAISES.items():
        df.loc[df["Pais_Upper"] == chave, "Pais"] = valor_padrao

    df = df.drop(columns=["Pais_Upper"])

    df_paises = df[~df["Pais"].str.upper().isin(CONTINENTES_E_TOTAIS)].copy()

    df_agrupado = (
        df_paises.groupby(["Ano", "Pais"])[["Total", "Aérea", "Marítima"]]
        .sum()
        .reset_index()
    )

    return df_agrupado


# ==============================================================================
# BARRA LATERAL (SIDEBAR)
# ==============================================================================
with st.sidebar:

    # ==========================================================================
    # Exercício 1. Escolha dos Datasets e Explicação do Objetivo e Motivação:
    # Escolha um ou mais datasets do portal Data Rio. Explique o objetivo e a
    # motivação por trás da escolha dos dados e quais funcionalidades e visualizações
    # serão implementadas.
    # ==========================================================================
    st.markdown("### ℹ️ Sobre o Dataset")
    st.markdown("""
    **Dataset**: Tabela 2674 - Chegada de turistas ao Rio de Janeiro por via de acesso (2006-2019).
    
    **Objetivo**: Analisar o fluxo de turistas internacionais no Rio de Janeiro discriminado por modais de entrada (aéreo e marítimo).
    
    **Motivação**: Mapear a dinâmica de receptivo internacional para subsidiar decisões estratégicas em turismo.
    """)

    st.markdown("---")

    # ==========================================================================
    # Exercício 2. Realizar Upload de Arquivo XLS:
    # Crie uma interface em Streamlit que permita ao usuário fazer o upload
    # de um arquivo XLS contendo dados de turismo do portal Data.Rio.
    # ==========================================================================
    st.markdown("### 📂 Entrada de Dados")
    arquivo_xls = st.file_uploader("Upload da Tabela 2674 (XLS)", type=["xls"])

    st.markdown("---")

    # ==========================================================================
    # Exercício 7. Utilizar Color Picker:
    # Adicione um color picker à interface que permita ao usuário personalizar
    # a cor de fundo do painel e das fontes exibidas na aplicação.
    # ==========================================================================
    st.markdown("### 🎨 Personalização de Aparência")
    cor_fundo = st.color_picker(
        "Cor de Fundo do Painel", st.session_state["bg_color"]
    )
    cor_titulo = st.color_picker(
        "Cor dos Títulos / Fontes", st.session_state["text_color"]
    )

    st.session_state["bg_color"] = cor_fundo
    st.session_state["text_color"] = cor_titulo


# Injeção dinâmica de CSS com base nos Color Pickers
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {st.session_state["bg_color"]} !important;
    }}
    .main h1, .main h2, .main h3, .main h4 {{
        color: {st.session_state["text_color"]} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 28px !important;
        font-weight: 700 !important;
        color: {st.session_state["text_color"]} !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: #1E1E2E !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #FFFFFF !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# TELA PRINCIPAL
# ==============================================================================
st.title("Painel Analítico de Turismo do Rio de Janeiro")
st.caption(
    "Monitoramento estratégico da entrada de turistas por modais (2006–2019)"
)

if arquivo_xls is not None:

    # ==========================================================================
    # Exercício 6. Utilizar Barra de Progresso e Spinners:
    # Adicione uma barra de progresso e um spinner para indicar o carregamento
    # dos dados enquanto o arquivo XLS é processado e exibido na interface.
    # ==========================================================================
    barra_progresso = st.progress(0)
    for p in range(0, 101, 25):
        time.sleep(0.02)
        barra_progresso.progress(p)

    with st.spinner("Processando base de dados do Data.Rio..."):
        df_completo = carregar_e_limpar_dados(arquivo_xls)
    barra_progresso.empty()

    # ==========================================================================
    # Exercício 3. Filtro de Dados e Seleção:
    # Exiba o dataset para o usuário e implemente três seletores diferentes
    # (radio, checkbox, dropdowns) na interface que permitam ao usuário filtrar
    # os dados carregados e selecionar as colunas ou linhas que deseja visualizar.
    # ==========================================================================
    st.subheader("Filtros de Pesquisa")
    c1, c2, c3 = st.columns([1, 1, 1.2])

    with c1:
        # Seletor 1: Radio Button (seleção da coluna/modal)
        via_selecionada = st.radio(
            "Via de Acesso:", ["Total", "Aérea", "Marítima"], horizontal=True
        )

    with c2:
        # Seletor 2: Dropdown / Selectbox (seleção de ano)
        anos_disponiveis = sorted(df_completo["Ano"].unique())
        ano_selecionado = st.selectbox(
            "Ano de Destaque:",
            anos_disponiveis,
            index=len(anos_disponiveis) - 1,
        )

    with c3:
        # Seletor 3: Checkbox + Dropdown (filtro opcional por país)
        filtrar_por_pais = st.checkbox("Filtrar País Específico")
        if filtrar_por_pais:
            paises_disponiveis = sorted(df_completo["Pais"].unique())
            pais_selecionado = st.selectbox("País:", paises_disponiveis)

    # Aplicação dos filtros selecionados
    df_ano_global = df_completo[df_completo["Ano"] == ano_selecionado]

    df_filtrado = df_completo.copy()
    if filtrar_por_pais:
        df_filtrado = df_filtrado[df_filtrado["Pais"] == pais_selecionado]

    # DataFrame totalmente filtrado (Ano + País/Global)
    df_ano_filtrado = df_filtrado[df_filtrado["Ano"] == ano_selecionado]

    st.markdown("---")

    # Organização das visualizações em abas
    tab_resumo, tab_graficos, tab_tabela = st.tabs(
        ["📊 Visão Geral & Métricas", "📈 Gráficos & Análises", "📋 Tabela & Download"]
    )

    # ABA 1: MÉTRICAS E GRÁFICO DE BARRAS
    with tab_resumo:

        # ======================================================================
        # Exercício 12. Exibir Métricas Básicas:
        # Implemente a exibição de métricas básicas (como contagem de registros,
        # médias, somas) diretamente na interface para fornecer um resumo
        # rápido dos dados carregados.
        # ======================================================================
        m1, m2, m3 = st.columns(3)

        if filtrar_por_pais:
            val_total_pais = (
                df_ano_filtrado[via_selecionada].sum()
                if not df_ano_filtrado.empty
                else 0
            )
            val_media_global = df_ano_global[via_selecionada].mean()

            total_fmt = f"{int(val_total_pais):,}".replace(",", ".")
            media_fmt = f"{int(val_media_global):,}".replace(",", ".")

            with m1:
                st.metric(
                    f"Total - {pais_selecionado} ({ano_selecionado})", total_fmt
                )
            with m2:
                st.metric(
                    f"Média Global dos Países ({ano_selecionado})", media_fmt
                )
            with m3:
                st.metric("País Selecionado", pais_selecionado)
        else:
            val_total_global = df_ano_global[via_selecionada].sum()
            val_media_global = df_ano_global[via_selecionada].mean()

            total_fmt = f"{int(val_total_global):,}".replace(",", ".")
            media_fmt = f"{int(val_media_global):,}".replace(",", ".")

            with m1:
                st.metric(
                    f"Total Global de Turistas ({ano_selecionado})", total_fmt
                )
            with m2:
                st.metric(f"Média por País ({ano_selecionado})", media_fmt)
            with m3:
                st.metric("Países Registrados", len(df_ano_global))

        st.markdown("---")

        # ======================================================================
        # Exercício 10. Criar Visualizações de Dados - Gráficos Simples (Barras):
        # Desenvolva gráficos simples (barras, linhas, e pie charts) para
        # visualização dos dados carregados, utilizando o Streamlit.
        # ======================================================================
        df_top10 = df_ano_global.nlargest(10, via_selecionada)
        fig_bar = px.bar(
            df_top10,
            x="Pais",
            y=via_selecionada,
            title=f"Top 10 Países Emissores no Ano de {ano_selecionado} (Via: {via_selecionada})",
            template="plotly_dark",
            color=via_selecionada,
            color_continuous_scale="Blues",
        )
        fig_bar.update_layout(margin=dict(l=20, r=20, t=50, b=20), height=420)
        st.plotly_chart(fig_bar, use_container_width=True)

    # ABA 2: GRÁFICOS DETALHADOS
    with tab_graficos:
        g1, g2 = st.columns(2)

        with g1:
            # ==================================================================
            # Exercício 10. Criar Visualizações de Dados - Gráficos Simples (Linhas):
            # ==================================================================
            df_linha = (
                df_filtrado.groupby("Ano")[via_selecionada].sum().reset_index()
            )
            fig_line = px.line(
                df_linha,
                x="Ano",
                y=via_selecionada,
                markers=True,
                title=f"Série Histórica (2006–2019) {'— ' + pais_selecionado if filtrar_por_pais else ''}",
                template="plotly_dark",
            )
            st.plotly_chart(fig_line, use_container_width=True)

            # ==================================================================
            # Exercício 11. Criar Visualizações de Dados - Gráficos Avançados (Histograma):
            # Adicione gráficos avançados (histograma e scatter plot) para fornecer
            # insights mais profundos sobre os dados.
            # ==================================================================
            fig_hist = px.histogram(
                df_filtrado,
                x=via_selecionada,
                nbins=15,
                title=f"Distribuição de Frequência — Modal {via_selecionada}",
                template="plotly_dark",
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with g2:
            # ==================================================================
            # Exercício 10. Criar Visualizações de Dados - Gráficos Simples (Pie Chart):
            # ==================================================================
            fig_pie = px.pie(
                df_top10,
                values=via_selecionada,
                names="Pais",
                title=f"Proporção Top 10 Países no Ano de {ano_selecionado} (Via: {via_selecionada})",
                hole=0.4,
                template="plotly_dark",
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            # ==================================================================
            # Exercício 11. Criar Visualizações de Dados - Gráficos Avançados (Scatter Plot):
            # ==================================================================
            fig_scatter = px.scatter(
                df_filtrado,
                x="Aérea",
                y="Marítima",
                size="Total",
                hover_name="Pais",
                color="Ano",
                title="Correlação entre Modais: Aéreo vs. Marítimo",
                template="plotly_dark",
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    # ABA 3: TABELA DE DADOS E SERVIÇO DE DOWNLOAD
    with tab_tabela:

        # ======================================================================
        # Exercício 4. Criar Visualizações de Dados - Tabelas:
        # Crie uma tabela interativa que exiba os dados filtrados de acordo com os
        # seletores carregados e permita ao usuário ordenar e filtrar as colunas
        # diretamente pela interface.
        # ======================================================================
        st.subheader("Dados Estruturados Filtrados")

        # Exibe unicamente o subset referente ao ano, via e país selecionados
        st.dataframe(
            df_ano_filtrado[["Ano", "Pais", via_selecionada]],
            use_container_width=True,
            height=350,
        )

        # ======================================================================
        # Exercício 5. Desenvolver Serviço de Download de Arquivos:
        # Implemente um serviço que permita ao usuário fazer o download dos dados
        # filtrados em formato XLS diretamente pela interface da aplicação.
        # ======================================================================
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_ano_filtrado.to_excel(writer, index=False)
        excel_data = buffer.getvalue()

        st.download_button(
            label="📥 Baixar Tabela Filtrada em Excel (.xlsx)",
            data=excel_data,
            file_name="turismo_rio_paises_filtrado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

else:
    st.info(
        "👈 Utilize o menu lateral para carregar o arquivo XLS do portal Data.Rio e iniciar a análise."
    )