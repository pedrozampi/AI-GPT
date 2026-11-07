"""Dashboard Comercial Multi-Lojas e Marcas — Neumorphism (Soft UI) Edition.

Aplicação analítica interativa desenvolvida em Streamlit e Plotly Express,
estilizada estritamente sob as especificações do Neumorphism Design System (style.md).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ==============================================================================
# DESIGN SYSTEM NEUMORPHISM (TOKENS CONFORME STYLE.MD)
# ==============================================================================
NEU_BG = "#e0e5ec"            # Fundo base e superfície principal
NEU_BG_LIGHT = "#f0f0f3"      # Superfície elevada / secundária
NEU_DARK_SHADOW = "#b8bcc2"   # Sombra inferior direita (+X, +Y)
NEU_LIGHT_SHADOW = "#ffffff"  # Sombra superior esquerda (-X, -Y)
NEU_ACCENT = "#6d5dfc"        # Cor de destaque, interações e CTAs
NEU_TEXT_PRIMARY = "#333333"  # Tipografia principal / cabeçalhos
NEU_TEXT_MUTED = "#6b7280"    # Rótulos, legendas e textos secundários

# Paleta suave e harmoniosa para gráficos sobre fundo neumórfico
NEU_COLOR_SEQUENCE = ["#6d5dfc", "#4ecdc4", "#ff6b6b", "#ffe66d", "#5b86e5", "#a29bfe"]


# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Dashboard Comercial Multi-Lojas | Soft UI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================================
# INJEÇÃO DO CSS NEUMÓRFICO (DUAL SHADOW & TACTILE DEPTH)
# ==============================================================================
NEU_CSS = f"""
<style>
/* 1. Base da aplicação */
.stApp {{
    background-color: {NEU_BG} !important;
    color: {NEU_TEXT_PRIMARY} !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}}

/* 2. Barra lateral neumórfica */
[data-testid="stSidebar"] {{
    background-color: {NEU_BG} !important;
    border-right: none !important;
    box-shadow: 4px 0 16px {NEU_DARK_SHADOW} !important;
}}
[data-testid="stSidebar"] * {{
    color: {NEU_TEXT_PRIMARY} !important;
}}

/* 3. Títulos e cabeçalhos */
h1, h2, h3, h4, h5, h6 {{
    color: {NEU_TEXT_PRIMARY} !important;
    font-weight: 600 !important;
}}

/* 4. Divisores sutis */
hr {{
    border: none !important;
    height: 2px !important;
    background-color: #d1d6de !important;
    box-shadow: 0 1px 1px {NEU_LIGHT_SHADOW} !important;
}}

/* 5. Cards de Métricas Neumórficos (Raised 3D) */
[data-testid="stMetric"] {{
    background-color: {NEU_BG} !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 18px 20px !important;
    box-shadow: 8px 8px 16px {NEU_DARK_SHADOW}, -8px -8px 16px {NEU_LIGHT_SHADOW} !important;
    transition: all 0.2s ease-in-out !important;
}}
[data-testid="stMetric"]:hover {{
    box-shadow: 4px 4px 8px {NEU_DARK_SHADOW}, -4px -4px 8px {NEU_LIGHT_SHADOW} !important;
}}
[data-testid="stMetricLabel"] p {{
    color: {NEU_TEXT_MUTED} !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}}
[data-testid="stMetricValue"] div {{
    color: {NEU_ACCENT} !important;
    font-size: 1.65rem !important;
    font-weight: 700 !important;
}}

/* 6. Inputs e Seletoras (Recessed / Inset) */
[data-baseweb="select"] > div, [data-baseweb="input"] > div, input {{
    background-color: {NEU_BG} !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: inset 4px 4px 8px {NEU_DARK_SHADOW}, inset -4px -4px 8px {NEU_LIGHT_SHADOW} !important;
    color: {NEU_TEXT_PRIMARY} !important;
}}
[data-baseweb="select"] span {{
    color: {NEU_TEXT_PRIMARY} !important;
}}

/* 7. Abas de Navegação Neumórficas */
.stTabs [data-baseweb="tab-list"] {{
    gap: 12px !important;
    background-color: transparent !important;
    border-bottom: none !important;
    padding: 10px 0 !important;
}}
.stTabs [data-baseweb="tab"] {{
    background-color: {NEU_BG} !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 10px 22px !important;
    color: {NEU_TEXT_MUTED} !important;
    font-weight: 600 !important;
    box-shadow: 6px 6px 12px {NEU_DARK_SHADOW}, -6px -6px 12px {NEU_LIGHT_SHADOW} !important;
    transition: all 0.2s ease-in-out !important;
}}
.stTabs [data-baseweb="tab"]:hover {{
    box-shadow: 3px 3px 6px {NEU_DARK_SHADOW}, -3px -3px 6px {NEU_LIGHT_SHADOW} !important;
}}
.stTabs [aria-selected="true"] {{
    background-color: {NEU_BG} !important;
    color: {NEU_ACCENT} !important;
    box-shadow: inset 4px 4px 8px {NEU_DARK_SHADOW}, inset -4px -4px 8px {NEU_LIGHT_SHADOW} !important;
    border: none !important;
}}

/* 8. Botões Neumórficos (Extrude to Intrude) */
.stButton > button, .stDownloadButton > button {{
    background-color: {NEU_BG} !important;
    color: {NEU_ACCENT} !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 10px 24px !important;
    box-shadow: 6px 6px 12px {NEU_DARK_SHADOW}, -6px -6px 12px {NEU_LIGHT_SHADOW} !important;
    transition: all 0.2s ease-in-out !important;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
    box-shadow: 3px 3px 6px {NEU_DARK_SHADOW}, -3px -3px 6px {NEU_LIGHT_SHADOW} !important;
    color: #5544e3 !important;
}}
.stButton > button:active, .stDownloadButton > button:active {{
    box-shadow: inset 4px 4px 8px {NEU_DARK_SHADOW}, inset -4px -4px 8px {NEU_LIGHT_SHADOW} !important;
}}

/* 9. Container Expansível */
[data-testid="stExpander"] {{
    background-color: {NEU_BG} !important;
    border: none !important;
    border-radius: 16px !important;
    box-shadow: 6px 6px 14px {NEU_DARK_SHADOW}, -6px -6px 14px {NEU_LIGHT_SHADOW} !important;
}}
[data-testid="stExpander"] summary {{
    color: {NEU_TEXT_PRIMARY} !important;
    font-weight: 600 !important;
}}

/* 10. Alertas suaves */
.stAlert {{
    border-radius: 14px !important;
    border: none !important;
    background-color: {NEU_BG} !important;
    box-shadow: 6px 6px 12px {NEU_DARK_SHADOW}, -6px -6px 12px {NEU_LIGHT_SHADOW} !important;
}}
</style>
"""
st.markdown(NEU_CSS, unsafe_allow_html=True)


# ==============================================================================
# FUNÇÕES DE FORMATAÇÃO E ESTILIZAÇÃO PLOTLY NEUMÓRFICA
# ==============================================================================
def format_currency(val: float) -> str:
    """Formata valor monetário no padrão brasileiro (R$ 1.234,56)."""
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_number(val: int | float) -> str:
    """Formata número inteiro ou decimal com separador de milhar brasileiro."""
    return f"{int(val):,}".replace(",", ".")


def apply_neumorphic_chart(fig: go.Figure) -> go.Figure:
    """Aplica estética Soft UI às figuras Plotly mantendo o fundo monocromático."""
    fig.update_layout(
        paper_bgcolor=NEU_BG,
        plot_bgcolor=NEU_BG,
        font=dict(color=NEU_TEXT_PRIMARY, family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"),
        title=dict(font=dict(color=NEU_TEXT_PRIMARY, size=15)),
        xaxis=dict(
            gridcolor="#d3d7de",
            zerolinecolor="#d3d7de",
            tickfont=dict(color=NEU_TEXT_MUTED),
            title=dict(font=dict(color=NEU_TEXT_PRIMARY)),
        ),
        yaxis=dict(
            gridcolor="#d3d7de",
            zerolinecolor="#d3d7de",
            tickfont=dict(color=NEU_TEXT_MUTED),
            title=dict(font=dict(color=NEU_TEXT_PRIMARY)),
        ),
        legend=dict(
            font=dict(color=NEU_TEXT_MUTED),
            title=dict(font=dict(color=NEU_TEXT_PRIMARY)),
        ),
    )
    return fig


# ==============================================================================
# PIPELINE DE CARREGAMENTO E ETL (EXTRAÇÃO, LIMPEZA E INTEGRAÇÃO)
# ==============================================================================
@st.cache_data
def load_and_clean_data() -> pd.DataFrame:
    """Carrega as tabelas relacionais em Excel, realiza limpeza de rodapés,

    tipagem, integridade matemática e consolidação dos relacionamentos.
    """
    base_dir = Path(__file__).parent
    clientes_path = base_dir / "Clientes.xlsx"
    lojas_marcas_path = base_dir / "Lojas_Marcas.xlsx"
    vendas_path = base_dir / "Vendas.xlsx"

    missing_files = []
    for p in [clientes_path, lojas_marcas_path, vendas_path]:
        if not p.exists():
            missing_files.append(p.name)

    if missing_files:
        raise FileNotFoundError(
            f"Arquivos obrigatórios não localizados: {', '.join(missing_files)}. "
            f"Certifique-se de que estão na pasta: {base_dir}"
        )

    # 1. Carregamento das tabelas
    df_clientes_raw = pd.read_excel(clientes_path, sheet_name="Clientes")
    df_marcas_raw = pd.read_excel(lojas_marcas_path, sheet_name="Marcas")
    df_lojas_raw = pd.read_excel(lojas_marcas_path, sheet_name="Lojas")
    df_vendas_raw = pd.read_excel(vendas_path, sheet_name="Vendas")

    # 2. Limpeza de rodapés explicativos e linhas de totais
    df_clientes = df_clientes_raw[
        pd.to_numeric(df_clientes_raw["ClienteID"], errors="coerce").notnull()
    ].copy()
    df_clientes["ClienteID"] = df_clientes["ClienteID"].astype(int)
    df_clientes["DataCadastro"] = pd.to_datetime(df_clientes["DataCadastro"], errors="coerce")
    df_clientes["NomeCliente"] = df_clientes["Nome"].astype(str).str.strip()
    df_clientes["Email"] = df_clientes["Email"].astype(str).str.strip()
    df_clientes["Cidade_Cliente"] = df_clientes["Cidade"].astype(str).str.strip()
    df_clientes["Estado_Cliente"] = df_clientes["Estado"].astype(str).str.strip()
    df_clientes = df_clientes[
        ["ClienteID", "NomeCliente", "Email", "Cidade_Cliente", "Estado_Cliente", "DataCadastro"]
    ]

    # Dimensão Marcas
    df_marcas = df_marcas_raw[
        pd.to_numeric(df_marcas_raw["MarcaID"], errors="coerce").notnull()
    ].copy()
    df_marcas["MarcaID"] = df_marcas["MarcaID"].astype(int)
    df_marcas["NomeMarca"] = df_marcas["NomeMarca"].astype(str).str.strip()
    df_marcas["Segmento"] = df_marcas["Segmento"].astype(str).str.strip()
    df_marcas = df_marcas[["MarcaID", "NomeMarca", "Segmento"]]

    # Dimensão Lojas
    df_lojas = df_lojas_raw[
        pd.to_numeric(df_lojas_raw["LojaID"], errors="coerce").notnull()
    ].copy()
    df_lojas["LojaID"] = df_lojas["LojaID"].astype(int)
    df_lojas["MarcaID"] = pd.to_numeric(df_lojas["MarcaID"], errors="coerce").fillna(0).astype(int)
    df_lojas["NomeLoja"] = df_lojas["NomeLoja"].astype(str).str.strip()
    df_lojas["Cidade_Loja"] = df_lojas["Cidade"].astype(str).str.strip()
    df_lojas["Estado_Loja"] = df_lojas["Estado"].astype(str).str.strip()
    df_lojas = df_lojas[["LojaID", "NomeLoja", "MarcaID", "Cidade_Loja", "Estado_Loja"]]

    # Tabela Fato Vendas
    df_vendas = df_vendas_raw[
        pd.to_numeric(df_vendas_raw["VendaID"], errors="coerce").notnull()
    ].copy()
    df_vendas["VendaID"] = df_vendas["VendaID"].astype(int)
    df_vendas["ClienteID"] = pd.to_numeric(df_vendas["ClienteID"], errors="coerce").fillna(0).astype(int)
    df_vendas["LojaID"] = pd.to_numeric(df_vendas["LojaID"], errors="coerce").fillna(0).astype(int)
    df_vendas["Data"] = pd.to_datetime(df_vendas["Data"], errors="coerce")
    df_vendas["Produto"] = df_vendas["Produto"].astype(str).str.strip()
    df_vendas["Quantidade"] = pd.to_numeric(df_vendas["Quantidade"], errors="coerce").fillna(0).astype(int)
    df_vendas["ValorUnitario"] = pd.to_numeric(df_vendas["ValorUnitario"], errors="coerce").fillna(0.0)
    df_vendas["ValorTotal"] = df_vendas["Quantidade"] * df_vendas["ValorUnitario"]

    # 3. Consolidação Relacional
    df_lojas_marcas = pd.merge(df_lojas, df_marcas, on="MarcaID", how="left")
    df_lojas_marcas["NomeMarca"] = df_lojas_marcas["NomeMarca"].fillna("Marca Não Informada")
    df_lojas_marcas["Segmento"] = df_lojas_marcas["Segmento"].fillna("Segmento Não Informado")

    merged = pd.merge(df_vendas, df_lojas_marcas, on="LojaID", how="left")
    merged["NomeLoja"] = merged["NomeLoja"].fillna("Loja Não Informada")
    merged["Cidade_Loja"] = merged["Cidade_Loja"].fillna("Não Informada")
    merged["Estado_Loja"] = merged["Estado_Loja"].fillna("Não Informado")

    merged = pd.merge(merged, df_clientes, on="ClienteID", how="left")
    merged["NomeCliente"] = merged["NomeCliente"].fillna("Cliente Desconhecido")
    merged["Email"] = merged["Email"].fillna("Não Informado")
    merged["Cidade_Cliente"] = merged["Cidade_Cliente"].fillna("Não Informada")
    merged["Estado_Cliente"] = merged["Estado_Cliente"].fillna("Não Informado")

    merged["AnoMes"] = merged["Data"].dt.to_period("M").astype(str)
    merged["MesAnoFormatado"] = merged["Data"].dt.strftime("%b/%Y")

    return merged


# ==============================================================================
# APLICAÇÃO PRINCIPAL
# ==============================================================================
def main():
    # Cabeçalho da Aplicação
    st.title("📊 Painel Comercial Multi-Lojas e Marcas")
    st.markdown(
        f"<span style='color:{NEU_TEXT_MUTED}; font-size:1.05rem;'>"
        "Ambiente analítico interativo sob as diretrizes do <b>Neumorphism Design System</b>, "
        "integrando o modelo relacional comercial (<i>Clientes, Lojas, Marcas e Vendas</i>).</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Carregamento seguro dos dados
    try:
        df = load_and_clean_data()
    except FileNotFoundError as err:
        st.error(f"⚠️ Erro ao carregar os dados: {err}")
        st.info("Verifique se as planilhas `Clientes.xlsx`, `Lojas_Marcas.xlsx` e `Vendas.xlsx` estão no diretório.")
        return
    except Exception as err:
        st.error(f"⚠️ Ocorreu um erro no processamento das tabelas: {err}")
        return

    # ==============================================================================
    # FILTROS DINÂMICOS NA BARRA LATERAL (SIDEBAR)
    # ==============================================================================
    st.sidebar.markdown(f"<h3 style='color:{NEU_TEXT_PRIMARY}; margin-bottom:15px;'>🔍 Filtros de Análise</h3>", unsafe_allow_html=True)

    # 1. Filtro por Período de Vendas
    min_date = df["Data"].min().date()
    max_date = df["Data"].max().date()

    date_range = st.sidebar.date_input(
        "📅 Período de Venda",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # 2. Filtro por Marca
    todas_marcas = sorted(df["NomeMarca"].unique().tolist())
    selected_marcas = st.sidebar.multiselect(
        "🏷️ Marcas",
        options=todas_marcas,
        default=todas_marcas,
    )

    # 3. Filtro por Segmento
    todos_segmentos = sorted(df["Segmento"].unique().tolist())
    selected_segmentos = st.sidebar.multiselect(
        "🎯 Segmento de Atuação",
        options=todos_segmentos,
        default=todos_segmentos,
    )

    # 4. Filtro por Loja (reativo às marcas e segmentos escolhidos)
    lojas_disponiveis = sorted(
        df[
            (df["NomeMarca"].isin(selected_marcas)) &
            (df["Segmento"].isin(selected_segmentos))
        ]["NomeLoja"].unique().tolist()
    )
    selected_lojas = st.sidebar.multiselect(
        "🏬 Unidades de Lojas",
        options=lojas_disponiveis,
        default=lojas_disponiveis,
    )

    # 5. Filtro por Cidade da Loja
    cidades_loja = sorted(df["Cidade_Loja"].unique().tolist())
    selected_cidades_loja = st.sidebar.multiselect(
        "📍 Cidade da Loja",
        options=cidades_loja,
        default=cidades_loja,
    )

    # 6. Filtro por Cliente
    todos_clientes = sorted(df["NomeCliente"].unique().tolist())
    selected_clientes = st.sidebar.multiselect(
        "👤 Clientes",
        options=todos_clientes,
        default=[],
        placeholder="Todos os clientes selecionados",
    )

    # Aplicação em cascata dos filtros no DataFrame
    filtered_df = df.copy()

    # Validação do intervalo de datas
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["Data"].dt.date >= start_date) &
            (filtered_df["Data"].dt.date <= end_date)
        ]
    elif isinstance(date_range, tuple) and len(date_range) == 1:
        start_date = date_range[0]
        filtered_df = filtered_df[filtered_df["Data"].dt.date >= start_date]

    if selected_marcas:
        filtered_df = filtered_df[filtered_df["NomeMarca"].isin(selected_marcas)]

    if selected_segmentos:
        filtered_df = filtered_df[filtered_df["Segmento"].isin(selected_segmentos)]

    if selected_lojas:
        filtered_df = filtered_df[filtered_df["NomeLoja"].isin(selected_lojas)]

    if selected_cidades_loja:
        filtered_df = filtered_df[filtered_df["Cidade_Loja"].isin(selected_cidades_loja)]

    if selected_clientes:
        filtered_df = filtered_df[filtered_df["NomeCliente"].isin(selected_clientes)]

    if filtered_df.empty:
        st.warning("⚠️ Nenhuma venda localizada para a combinação de filtros selecionada. Ajuste as opções na barra lateral.")
        return

    # ==============================================================================
    # CARDS DE KPIS EXECUTIVOS COM RELEVO NEUMÓRFICO
    # ==============================================================================
    faturamento_total = filtered_df["ValorTotal"].sum()
    volume_itens = filtered_df["Quantidade"].sum()
    total_transacoes = filtered_df["VendaID"].nunique()
    ticket_medio = faturamento_total / total_transacoes if total_transacoes > 0 else 0.0
    clientes_ativos = filtered_df["ClienteID"].nunique()
    media_itens_venda = volume_itens / total_transacoes if total_transacoes > 0 else 0.0

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    with kpi1:
        st.metric("💰 Faturamento Total", format_currency(faturamento_total))
    with kpi2:
        st.metric("📦 Volume Vendido", format_number(volume_itens))
    with kpi3:
        st.metric("🧾 Total de Transações", format_number(total_transacoes))
    with kpi4:
        st.metric("🎯 Ticket Médio", format_currency(ticket_medio))
    with kpi5:
        st.metric("👥 Clientes Ativos", format_number(clientes_ativos))
    with kpi6:
        st.metric("🛍️ Média Itens/Venda", f"{media_itens_venda:.1f}")

    st.markdown("---")

    # ==============================================================================
    # NAVEGAÇÃO EM ABAS TEMÁTICAS NEUMÓRFICAS
    # ==============================================================================
    tab_marcas, tab_lojas, tab_produtos, tab_clientes = st.tabs([
        "🏷️ Desempenho & Marcas",
        "🏬 Lojas & Análise Geográfica",
        "📦 Produtos & Sensibilidade",
        "👥 Visão Clientes & Base Analítica",
    ])

    # ------------------------------------------------------------------------------
    # ABA 1: DESEMPENHO COMERCIAL & MARCAS
    # ------------------------------------------------------------------------------
    with tab_marcas:
        col_m1, col_m2 = st.columns([1.5, 1])

        with col_m1:
            st.subheader("📈 Evolução Mensal do Faturamento")
            df_tempo = (
                filtered_df.groupby(["AnoMes", "NomeMarca"])["ValorTotal"]
                .sum()
                .reset_index()
                .sort_values(by="AnoMes")
            )
            fig_tempo = px.bar(
                df_tempo,
                x="AnoMes",
                y="ValorTotal",
                color="NomeMarca",
                barmode="stack",
                title="Faturamento Mensal por Marca",
                labels={"AnoMes": "Mês de Referência", "ValorTotal": "Faturamento (R$)", "NomeMarca": "Marca"},
                color_discrete_sequence=NEU_COLOR_SEQUENCE,
            )
            fig_tempo = apply_neumorphic_chart(fig_tempo)
            fig_tempo.update_layout(
                xaxis_title="Período (Ano-Mês)",
                yaxis_title="Faturamento (R$)",
                margin=dict(l=10, r=10, t=40, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            st.plotly_chart(fig_tempo, use_container_width=True)

        with col_m2:
            st.subheader("🍕 Participação por Segmento")
            df_segmento = (
                filtered_df.groupby("Segmento")["ValorTotal"]
                .sum()
                .reset_index()
                .sort_values(by="ValorTotal", ascending=False)
            )
            fig_seg = px.pie(
                df_segmento,
                names="Segmento",
                values="ValorTotal",
                hole=0.48,
                title="Receita por Segmento de Mercado",
                color_discrete_sequence=NEU_COLOR_SEQUENCE,
            )
            fig_seg = apply_neumorphic_chart(fig_seg)
            fig_seg.update_traces(
                textposition="inside",
                textinfo="percent+label",
                marker=dict(line=dict(color=NEU_BG, width=2)),
            )
            fig_seg.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_seg, use_container_width=True)

        st.markdown("#### Faturamento e Volume por Marca Comercial")
        df_marcas_summary = (
            filtered_df.groupby("NomeMarca")
            .agg(
                Faturamento=("ValorTotal", "sum"),
                Unidades=("Quantidade", "sum"),
                Transacoes=("VendaID", "nunique"),
            )
            .reset_index()
            .sort_values(by="Faturamento", ascending=True)
        )
        fig_marcas = px.bar(
            df_marcas_summary,
            x="Faturamento",
            y="NomeMarca",
            orientation="h",
            color="NomeMarca",
            color_discrete_sequence=NEU_COLOR_SEQUENCE,
            title="Ranking de Faturamento por Marca",
            labels={"NomeMarca": "Marca", "Faturamento": "Faturamento (R$)"},
            hover_data=["Unidades", "Transacoes"],
        )
        fig_marcas = apply_neumorphic_chart(fig_marcas)
        fig_marcas.update_layout(margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
        st.plotly_chart(fig_marcas, use_container_width=True)

    # ------------------------------------------------------------------------------
    # ABA 2: LOJAS & ANÁLISE GEOGRÁFICA
    # ------------------------------------------------------------------------------
    with tab_lojas:
        col_l1, col_l2 = st.columns([1.3, 1])

        with col_l1:
            st.subheader("🏬 Receita por Unidade de Loja")
            df_lojas_rank = (
                filtered_df.groupby(["NomeLoja", "Cidade_Loja", "NomeMarca"])
                .agg(
                    Faturamento=("ValorTotal", "sum"),
                    Volume=("Quantidade", "sum"),
                    Vendas=("VendaID", "nunique"),
                )
                .reset_index()
                .sort_values(by="Faturamento", ascending=False)
            )
            fig_lojas = px.bar(
                df_lojas_rank,
                x="NomeLoja",
                y="Faturamento",
                color="Cidade_Loja",
                title="Desempenho Financeiro por Loja Física",
                labels={"NomeLoja": "Loja", "Faturamento": "Faturamento (R$)", "Cidade_Loja": "Cidade da Loja"},
                hover_data=["NomeMarca", "Volume", "Vendas"],
                color_discrete_sequence=["#6d5dfc", "#4ecdc4"],
            )
            fig_lojas = apply_neumorphic_chart(fig_lojas)
            fig_lojas.update_layout(
                xaxis_tickangle=-30,
                xaxis_title=None,
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig_lojas, use_container_width=True)

        with col_l2:
            st.subheader("🌐 Cidades das Lojas vs Clientes")
            df_cidade_loja = (
                filtered_df.groupby("Cidade_Loja")["ValorTotal"]
                .sum()
                .reset_index()
                .rename(columns={"Cidade_Loja": "Cidade", "ValorTotal": "Faturamento Loja"})
            )
            df_cidade_cli = (
                filtered_df.groupby("Cidade_Cliente")["ValorTotal"]
                .sum()
                .reset_index()
                .rename(columns={"Cidade_Cliente": "Cidade", "ValorTotal": "Faturamento Cliente"})
            )
            df_geo_comp = pd.merge(df_cidade_loja, df_cidade_cli, on="Cidade", how="outer").fillna(0.0)

            fig_geo_comp = px.bar(
                df_geo_comp,
                x="Cidade",
                y=["Faturamento Loja", "Faturamento Cliente"],
                barmode="group",
                title="Fluxo Financeiro: Onde Comprou vs Residência",
                labels={"value": "Total (R$)", "variable": "Perspectiva"},
                color_discrete_map={"Faturamento Loja": "#6d5dfc", "Faturamento Cliente": "#ff6b6b"},
            )
            fig_geo_comp = apply_neumorphic_chart(fig_geo_comp)
            fig_geo_comp.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_geo_comp, use_container_width=True)

        st.markdown("#### Detalhamento de Performance por Unidade")
        st.dataframe(
            df_lojas_rank.rename(columns={
                "NomeLoja": "Loja",
                "Cidade_Loja": "Cidade",
                "NomeMarca": "Marca",
                "Faturamento": "Faturamento Bruto",
                "Volume": "Qtd Itens",
                "Vendas": "Qtd Pedidos",
            }),
            column_config={
                "Faturamento Bruto": st.column_config.NumberColumn("Faturamento", format="R$ %.2f"),
                "Qtd Itens": st.column_config.NumberColumn("Unidades", format="%d"),
                "Qtd Pedidos": st.column_config.NumberColumn("Transações", format="%d"),
            },
            use_container_width=True,
            hide_index=True,
        )

    # ------------------------------------------------------------------------------
    # ABA 3: PRODUTOS & SENSIBILIDADE
    # ------------------------------------------------------------------------------
    with tab_produtos:
        col_p1, col_p2 = st.columns([1.2, 1])

        with col_p1:
            st.subheader("🏆 Top Produtos por Faturamento")
            df_prod = (
                filtered_df.groupby(["Produto", "Segmento"])
                .agg(
                    Faturamento=("ValorTotal", "sum"),
                    Volume=("Quantidade", "sum"),
                    PrecoMedio=("ValorUnitario", "mean"),
                )
                .reset_index()
                .sort_values(by="Faturamento", ascending=True)
            )
            fig_prod = px.bar(
                df_prod,
                x="Faturamento",
                y="Produto",
                orientation="h",
                color="Segmento",
                title="Receita Gerada por Produto",
                labels={"Produto": "Item", "Faturamento": "Faturamento (R$)"},
                hover_data=["Volume", "PrecoMedio"],
                color_discrete_sequence=NEU_COLOR_SEQUENCE,
            )
            fig_prod = apply_neumorphic_chart(fig_prod)
            fig_prod.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_prod, use_container_width=True)

        with col_p2:
            st.subheader("🎯 Sensibilidade: Preço vs Quantidade")
            fig_scatter = px.scatter(
                filtered_df,
                x="ValorUnitario",
                y="Quantidade",
                color="Segmento",
                size="ValorTotal",
                hover_name="Produto",
                hover_data=["NomeLoja", "NomeCliente"],
                title="Dispersão: Preço Unitário vs Quantidade por Venda",
                labels={"ValorUnitario": "Preço Unitário (R$)", "Quantidade": "Qtd Vendida"},
                color_discrete_sequence=NEU_COLOR_SEQUENCE,
            )
            fig_scatter = apply_neumorphic_chart(fig_scatter)
            fig_scatter.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_scatter, use_container_width=True)

    # ------------------------------------------------------------------------------
    # ABA 4: VISÃO DOS CLIENTES & BASE ANALÍTICA
    # ------------------------------------------------------------------------------
    with tab_clientes:
        col_c1, col_c2 = st.columns([1.3, 1])

        with col_c1:
            st.subheader("⭐ Maiores Compradores (Top Clientes)")
            df_top_clientes = (
                filtered_df.groupby(["ClienteID", "NomeCliente", "Cidade_Cliente", "Email"])
                .agg(
                    TotalGasto=("ValorTotal", "sum"),
                    TotalPedidos=("VendaID", "nunique"),
                    TotalItens=("Quantidade", "sum"),
                )
                .reset_index()
                .sort_values(by="TotalGasto", ascending=False)
            )
            fig_top_cli = px.bar(
                df_top_clientes.head(10),
                x="NomeCliente",
                y="TotalGasto",
                color="Cidade_Cliente",
                title="Top 10 Clientes por Volume Financeiro",
                labels={"NomeCliente": "Cliente", "TotalGasto": "Total Comprado (R$)", "Cidade_Cliente": "Cidade"},
                hover_data=["TotalPedidos", "TotalItens", "Email"],
                color_discrete_sequence=NEU_COLOR_SEQUENCE,
            )
            fig_top_cli = apply_neumorphic_chart(fig_top_cli)
            fig_top_cli.update_layout(xaxis_tickangle=-30, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_top_cli, use_container_width=True)

        with col_c2:
            st.subheader("📍 Clientes Ativos por Município")
            df_cli_cid = (
                filtered_df.groupby("Cidade_Cliente")["ClienteID"]
                .nunique()
                .reset_index()
                .rename(columns={"Cidade_Cliente": "Cidade", "ClienteID": "Clientes Ativos"})
                .sort_values(by="Clientes Ativos", ascending=False)
            )
            fig_cli_cid = px.pie(
                df_cli_cid,
                names="Cidade",
                values="Clientes Ativos",
                hole=0.45,
                title="Distribuição de Clientes por Cidade",
                color_discrete_sequence=NEU_COLOR_SEQUENCE,
            )
            fig_cli_cid = apply_neumorphic_chart(fig_cli_cid)
            fig_cli_cid.update_traces(
                textposition="inside",
                textinfo="percent+label",
                marker=dict(line=dict(color=NEU_BG, width=2)),
            )
            fig_cli_cid.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_cli_cid, use_container_width=True)

        st.markdown("---")
        # Visualização e download da base tratada consolidada
        with st.expander("📋 Exibir Tabela de Dados Consolidados & Exportação CSV"):
            colunas_exibicao = [
                "VendaID", "Data", "Produto", "Quantidade", "ValorUnitario", "ValorTotal",
                "NomeLoja", "Cidade_Loja", "NomeMarca", "Segmento",
                "NomeCliente", "Cidade_Cliente", "Email"
            ]
            df_export = filtered_df[colunas_exibicao].sort_values(by="Data", ascending=False)

            st.dataframe(
                df_export,
                column_config={
                    "ValorUnitario": st.column_config.NumberColumn("Valor Unit.", format="R$ %.2f"),
                    "ValorTotal": st.column_config.NumberColumn("Valor Total", format="R$ %.2f"),
                    "Data": st.column_config.DatetimeColumn("Data", format="DD/MM/YYYY"),
                },
                use_container_width=True,
                hide_index=True,
            )

            csv_bytes = df_export.to_csv(index=False, sep=";").encode("utf-8-sig")
            st.download_button(
                label="📥 Baixar Base Consolidada Filtrada (CSV)",
                data=csv_bytes,
                file_name="vendas_consolidadas_filtradas.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    main()
