"""Dashboard de Vendas e Auditoria de Qualidade de Dados — Vaporwave / Neon Retro Edition.

Aplicação analítica com navegação por abas na barra lateral e modal de filtros sob demanda,
estilizada rigorosamente sob o Vaporwave / Neon Retro Design System (style.md).
"""

from pathlib import Path
from typing import Dict, Tuple, Any
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ==============================================================================
# DESIGN SYSTEM VAPORWAVE / NEON RETRO (TOKENS CONFORME STYLE.MD)
# ==============================================================================
VAPOR_BG = "#1a0a2e"            # Fundo principal (Midnight Deep Purple)
VAPOR_BG_PANEL = "#230c3c"      # Fundo dos painéis e cards
VAPOR_PINK = "#ff71ce"          # Neon Pink primário (Headlines e texto de destaque)
VAPOR_CYAN = "#01cdfe"          # Neon Cyan (Links, KPIs, acentos e bordas)
VAPOR_PURPLE = "#b967ff"        # Neon Purple secundário (Rótulos e legendas)
VAPOR_GREEN = "#05ffa1"         # Neon Green (Badges positivos e destaques)
VAPOR_YELLOW = "#fffb96"        # Neon Yellow (Alertas e elementos especiais)
VAPOR_TEXT_LIGHT = "#f8f0fb"    # Texto claro legível

# Paleta cromática de alta energia para gráficos Plotly
VAPOR_COLOR_SEQUENCE = ["#ff71ce", "#01cdfe", "#05ffa1", "#fffb96", "#b967ff"]
VAPOR_CONTINUOUS_SCALE = [
    [0.0, "#4a126d"],
    [0.35, "#b967ff"],
    [0.7, "#ff71ce"],
    [1.0, "#01cdfe"],
]


# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Painel de Vendas de Tecnologia | Data Quality",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================================
# INJEÇÃO DE CSS VAPORWAVE / NEON RETRO COM SUPORTE A MODAL E ABAS LATERAIS
# ==============================================================================
VAPOR_CSS = f"""
<style>
/* 1. Fundo base com Grid Retro-Futurista */
.stApp {{
    background-color: {VAPOR_BG} !important;
    background-image: 
        linear-gradient(rgba(255, 113, 206, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(1, 205, 254, 0.08) 1px, transparent 1px) !important;
    background-size: 40px 40px !important;
    color: {VAPOR_TEXT_LIGHT} !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}}

/* 2. Barra lateral Neon Retro */
[data-testid="stSidebar"] {{
    background-color: #16082a !important;
    background-image: 
        linear-gradient(rgba(255, 113, 206, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(1, 205, 254, 0.05) 1px, transparent 1px) !important;
    background-size: 30px 30px !important;
    border-right: 1px solid rgba(255, 113, 206, 0.4) !important;
    box-shadow: 4px 0 25px rgba(255, 113, 206, 0.25) !important;
}}
[data-testid="stSidebar"] * {{
    color: {VAPOR_PINK} !important;
}}

/* 3. Títulos em Gradiente Neon e Glow */
h1 {{
    background: linear-gradient(90deg, {VAPOR_PINK}, {VAPOR_PURPLE}, {VAPOR_CYAN}) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 900 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    filter: drop-shadow(0 0 15px rgba(255, 113, 206, 0.4));
}}
h2, h3, h4 {{
    color: {VAPOR_CYAN} !important;
    font-weight: 700 !important;
    text-shadow: 0 0 10px rgba(1, 205, 254, 0.5) !important;
    letter-spacing: 1px !important;
}}

/* 4. Divisores em Neon Rosa */
hr {{
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, transparent, {VAPOR_PINK}, {VAPOR_CYAN}, transparent) !important;
    box-shadow: 0 0 12px {VAPOR_PINK} !important;
}}

/* 5. Cards de Métricas (Dual-Color Neon Glow) */
[data-testid="stMetric"] {{
    background: rgba(35, 12, 60, 0.88) !important;
    border: 1px solid rgba(255, 113, 206, 0.45) !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    box-shadow: 0 0 15px rgba(255, 113, 206, 0.3), 0 0 25px rgba(1, 205, 254, 0.15) !important;
    transition: all 0.3s ease-in-out !important;
}}
[data-testid="stMetric"]:hover {{
    box-shadow: 0 0 25px rgba(1, 205, 254, 0.6), 0 0 35px rgba(255, 113, 206, 0.4) !important;
    border-color: {VAPOR_CYAN} !important;
    transform: translateY(-2px);
}}
[data-testid="stMetricLabel"] p {{
    color: {VAPOR_PURPLE} !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}}
[data-testid="stMetricValue"] div {{
    color: {VAPOR_CYAN} !important;
    text-shadow: 0 0 10px rgba(1, 205, 254, 0.7) !important;
    font-size: 1.7rem !important;
    font-weight: 800 !important;
}}

/* 6. Navegação da Sidebar (Abas em Formato de Cartucho Neon) */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {{
    gap: 10px !important;
}}
[data-testid="stSidebar"] [data-testid="stRadio"] label {{
    background: rgba(35, 12, 60, 0.75) !important;
    border: 1px solid rgba(255, 113, 206, 0.35) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    transition: all 0.25s ease-in-out !important;
    cursor: pointer !important;
    box-shadow: 0 0 10px rgba(255, 113, 206, 0.15) !important;
}}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
    border-color: {VAPOR_CYAN} !important;
    box-shadow: 0 0 22px rgba(1, 205, 254, 0.5) !important;
    transform: translateX(4px) !important;
}}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{
    background: linear-gradient(90deg, rgba(255, 113, 206, 0.85), rgba(185, 103, 255, 0.85)) !important;
    border-color: {VAPOR_CYAN} !important;
    box-shadow: 0 0 25px rgba(255, 113, 206, 0.7) !important;
}}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {{
    color: #ffffff !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
}}

/* 7. Botões e Ações */
.stButton > button, .stDownloadButton > button {{
    background: linear-gradient(90deg, {VAPOR_PINK}, {VAPOR_PURPLE}) !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
    border-radius: 10px !important;
    border: 1px solid rgba(1, 205, 254, 0.6) !important;
    padding: 10px 24px !important;
    box-shadow: 0 0 16px rgba(255, 113, 206, 0.6) !important;
    transition: all 0.3s ease-in-out !important;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{
    box-shadow: 0 0 30px rgba(1, 205, 254, 0.8), 0 0 20px rgba(255, 113, 206, 0.6) !important;
    border-color: {VAPOR_CYAN} !important;
    transform: translateY(-2px);
}}

/* 8. Estilo do Modal de Filtros (Dialog) */
[data-testid="stModal"] > div:first-child, div[role="dialog"] {{
    background-color: {VAPOR_BG} !important;
    background-image: 
        linear-gradient(rgba(255, 113, 206, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(1, 205, 254, 0.08) 1px, transparent 1px) !important;
    background-size: 30px 30px !important;
    border: 2px solid {VAPOR_PINK} !important;
    border-radius: 16px !important;
    box-shadow: 0 0 40px rgba(255, 113, 206, 0.6), 0 0 80px rgba(1, 205, 254, 0.4) !important;
    color: {VAPOR_TEXT_LIGHT} !important;
}}
[data-testid="stModal"] h2, div[role="dialog"] h2 {{
    color: {VAPOR_PINK} !important;
    text-shadow: 0 0 10px rgba(255, 113, 206, 0.7) !important;
    font-weight: 900 !important;
}}

/* 9. Inputs e Seletoras */
[data-baseweb="select"] > div, [data-baseweb="input"] > div, input {{
    background-color: rgba(22, 8, 42, 0.9) !important;
    border: 1px solid rgba(255, 113, 206, 0.4) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 10px rgba(255, 113, 206, 0.2) !important;
    color: #ffffff !important;
}}
[data-baseweb="select"] span {{
    color: #ffffff !important;
}}

/* 10. Container Expansível e DataFrames */
[data-testid="stExpander"] {{
    background: rgba(35, 12, 60, 0.85) !important;
    border: 1px solid rgba(255, 113, 206, 0.35) !important;
    border-radius: 14px !important;
    box-shadow: 0 0 15px rgba(255, 113, 206, 0.25) !important;
}}
[data-testid="stExpander"] summary {{
    color: {VAPOR_CYAN} !important;
    font-weight: 700 !important;
}}
[data-testid="stDataFrame"] {{
    border: 1px solid rgba(255, 113, 206, 0.35) !important;
    border-radius: 12px !important;
    box-shadow: 0 0 15px rgba(255, 113, 206, 0.2) !important;
}}
</style>
"""
st.markdown(VAPOR_CSS, unsafe_allow_html=True)


# ==============================================================================
# FUNÇÕES DE FORMATAÇÃO E ESTILIZAÇÃO PLOTLY VAPORWAVE
# ==============================================================================
def format_currency(val: float) -> str:
    """Formata valor numérico no padrão monetário brasileiro (R$ 1.234,56)."""
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_number(val: int | float) -> str:
    """Formata número inteiro ou float com separador de milhar brasileiro."""
    return f"{int(val):,}".replace(",", ".")


def format_cpf(val: Any) -> str:
    """Higieniza e aplica máscara padrão de CPF (000.000.000-00) ou sinaliza ausência."""
    if pd.isna(val) or not str(val).strip():
        return "NÃO INFORMADO"
    digits = "".join(filter(str.isdigit, str(val))).zfill(11)
    if len(digits) != 11:
        return f"INVÁLIDO ({val})"
    return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"


def apply_vaporwave_chart(fig: go.Figure) -> go.Figure:
    """Aplica estética Vaporwave / Neon Retro às figuras do Plotly."""
    fig.update_layout(
        paper_bgcolor="rgba(26, 10, 46, 0.85)",
        plot_bgcolor="rgba(26, 10, 46, 0.85)",
        font=dict(color=VAPOR_PINK, family="-apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"),
        title=dict(font=dict(color=VAPOR_CYAN, size=15)),
        xaxis=dict(
            gridcolor="rgba(255, 113, 206, 0.15)",
            zerolinecolor="rgba(1, 205, 254, 0.3)",
            tickfont=dict(color=VAPOR_CYAN),
            title=dict(font=dict(color=VAPOR_PINK)),
        ),
        yaxis=dict(
            gridcolor="rgba(255, 113, 206, 0.15)",
            zerolinecolor="rgba(1, 205, 254, 0.3)",
            tickfont=dict(color=VAPOR_CYAN),
            title=dict(font=dict(color=VAPOR_PINK)),
        ),
        legend=dict(
            font=dict(color=VAPOR_PINK),
            title=dict(font=dict(color=VAPOR_CYAN)),
        ),
    )
    return fig


# ==============================================================================
# PIPELINE DE CARREGAMENTO, AUDITORIA E SANEAMENTO (ETL)
# ==============================================================================
@st.cache_data
def load_and_clean_data() -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Carrega dados_vendas_problemas.csv com encoding latin-1, audita anomalias,

    remove duplicatas de negócio, higieniza tipos e formatações.
    """
    base_dir = Path(__file__).parent
    csv_path = base_dir / "dados_vendas_problemas.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Arquivo de dados não encontrado: '{csv_path.name}' no diretório: {base_dir}"
        )

    df_raw = pd.read_csv(csv_path, encoding="latin-1", sep=",")
    total_raw = len(df_raw)

    cpfs_vazios = df_raw["cpf"].isna().sum() + (df_raw["cpf"].astype(str).str.strip() == "").sum()

    dup_subset = ["nome_cliente", "cpf", "data_venda", "cidade", "produto", "quantidade", "valor_total"]
    duplicated_mask = df_raw.duplicated(subset=dup_subset, keep=False)
    df_duplicadas = df_raw[duplicated_mask].sort_values(by=["cpf", "data_venda"]).copy()
    qtd_duplicatas_removidas = df_raw.duplicated(subset=dup_subset, keep="first").sum()

    df = df_raw.drop_duplicates(subset=dup_subset, keep="first").copy()

    for col in ["nome_cliente", "cidade", "produto"]:
        df[col] = df[col].astype(str).str.strip().str.title()

    df["cpf_formatado"] = df["cpf"].apply(format_cpf)
    df["cpf_valido"] = df["cpf_formatado"] != "NÃO INFORMADO"

    df["data_venda"] = pd.to_datetime(df["data_venda"], format="%d/%m/%Y", errors="coerce")
    df["AnoMes"] = df["data_venda"].dt.to_period("M").astype(str)
    df["MesAno"] = df["data_venda"].dt.strftime("%b/%Y")

    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce").fillna(0).astype(int)
    df["valor_unitario"] = pd.to_numeric(df["valor_unitario"], errors="coerce").fillna(0.0)

    df["valor_total_calculado"] = df["quantidade"] * df["valor_unitario"]
    df["valor_total"] = df["valor_total_calculado"]

    audit_metrics = {
        "total_registros_brutos": total_raw,
        "duplicatas_removidas": int(qtd_duplicatas_removidas),
        "cpfs_ausentes_tratados": int(cpfs_vazios),
        "total_registros_higienizados": len(df),
        "df_duplicadas": df_duplicadas,
    }

    return df, audit_metrics


# ==============================================================================
# INTERFACE PRINCIPAL
# ==============================================================================
def main():
    # Cabeçalho com identificação clara do domínio dos dados
    st.markdown(
        f"<div style='margin-bottom: 5px; font-size: 0.85rem; letter-spacing: 2px; color: {VAPOR_PURPLE}; font-weight: bold;'>"
        "VAREJO DE ELETRÔNICOS E INFORMÁTICA // AUDITORIA TRANSACIONAL"
        "</div>",
        unsafe_allow_html=True,
    )
    st.title("Painel de Vendas e Auditoria de Pedidos")
    st.markdown(
        f"<span style='color:{VAPOR_CYAN}; font-size:1.02rem; text-shadow: 0 0 6px rgba(1, 205, 254, 0.4);'>"
        "Monitoramento de transações comerciais de produtos de informática (<i>Notebooks, Monitores, Teclados e Mouses</i>), "
        "com pipeline de saneamento cadastral, deduplicação de pedidos e análise de faturamento por município.</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Carregamento seguro dos dados
    try:
        df, audit = load_and_clean_data()
    except FileNotFoundError as err:
        st.error(f"Erro no carregamento: {err}")
        st.info("Certifique-se de que o arquivo dados_vendas_problemas.csv está na pasta do exercício.")
        return
    except Exception as err:
        st.error(f"Ocorreu uma falha no processamento do arquivo: {err}")
        return

    # Limites e listas de referência para filtros
    min_date = df["data_venda"].min().date()
    max_date = df["data_venda"].max().date()
    todos_produtos = sorted(df["produto"].unique().tolist())
    todas_cidades = sorted(df["cidade"].unique().tolist())
    todos_clientes = sorted(df["nome_cliente"].unique().tolist())

    # Inicialização do session_state para manter os filtros ativos
    if "filter_date_range" not in st.session_state:
        st.session_state["filter_date_range"] = (min_date, max_date)
    if "filter_produtos" not in st.session_state:
        st.session_state["filter_produtos"] = todos_produtos
    if "filter_cidades" not in st.session_state:
        st.session_state["filter_cidades"] = todas_cidades
    if "filter_clientes" not in st.session_state:
        st.session_state["filter_clientes"] = []
    if "filter_cpf" not in st.session_state:
        st.session_state["filter_cpf"] = "Todos os Registros"

    # ==============================================================================
    # SIDEBAR: ABAS DE NAVEGAÇÃO E BOTÃO MODAL DE FILTROS
    # ==============================================================================
    st.sidebar.markdown(
        f"<div style='letter-spacing:1.5px; font-size:0.85rem; color:{VAPOR_PURPLE}; font-weight:800; margin-bottom:8px;'>"
        "PAINEL DE NAVEGAÇÃO"
        "</div>",
        unsafe_allow_html=True,
    )

    # 1. Abas na Sidebar (Radio estilizado sem emotes)
    nav_tabs = [
        "Visão Geral e Produtos",
        "Desempenho Geográfico",
        "Perfil dos Compradores",
        "Auditoria e Qualidade ETL",
    ]
    aba_selecionada = st.sidebar.radio(
        "VISÃO DO DASHBOARD:",
        options=nav_tabs,
        index=0,
        label_visibility="collapsed",
    )

    st.sidebar.markdown("---")

    # 2. Seção de Filtros dentro de um Botão / Modal
    st.sidebar.markdown(
        f"<div style='letter-spacing:1px; font-size:0.85rem; color:{VAPOR_CYAN}; font-weight:800; margin-bottom:10px;'>"
        "CONTROLE DE FILTROS"
        "</div>",
        unsafe_allow_html=True,
    )

    # Função que renderiza o formulário de filtros
    def render_filters_form():
        st.markdown(
            f"<div style='color:{VAPOR_PINK}; font-size:0.95rem; margin-bottom:12px;'>"
            "Ajuste os parâmetros de busca para filtrar as vendas por período, produtos e localidades:</div>",
            unsafe_allow_html=True,
        )

        f_date = st.date_input(
            "Período da Transação",
            value=st.session_state["filter_date_range"],
            min_value=min_date,
            max_value=max_date,
            key="_temp_date_range",
        )

        f_prod = st.multiselect(
            "Produtos",
            options=todos_produtos,
            default=st.session_state["filter_produtos"],
            key="_temp_produtos",
        )

        f_cid = st.multiselect(
            "Cidades",
            options=todas_cidades,
            default=st.session_state["filter_cidades"],
            key="_temp_cidades",
        )

        f_cli = st.multiselect(
            "Clientes Específicos",
            options=todos_clientes,
            default=st.session_state["filter_clientes"],
            placeholder="Todos os clientes ativos",
            key="_temp_clientes",
        )

        f_cpf = st.radio(
            "Integridade de CPF:",
            options=["Todos os Registros", "Apenas CPFs Válidos", "Apenas CPFs Não Informados"],
            index=["Todos os Registros", "Apenas CPFs Válidos", "Apenas CPFs Não Informados"].index(
                st.session_state["filter_cpf"]
            ),
            key="_temp_cpf",
        )

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        col_m_btn1, col_m_btn2 = st.columns(2)
        with col_m_btn1:
            if st.button("Aplicar Filtros", use_container_width=True):
                st.session_state["filter_date_range"] = f_date
                st.session_state["filter_produtos"] = f_prod
                st.session_state["filter_cidades"] = f_cid
                st.session_state["filter_clientes"] = f_cli
                st.session_state["filter_cpf"] = f_cpf
                st.rerun()

        with col_m_btn2:
            if st.button("Restaurar Padrão", use_container_width=True):
                st.session_state["filter_date_range"] = (min_date, max_date)
                st.session_state["filter_produtos"] = todos_produtos
                st.session_state["filter_cidades"] = todas_cidades
                st.session_state["filter_clientes"] = []
                st.session_state["filter_cpf"] = "Todos os Registros"
                st.rerun()

    # Disparo do Modal (ou Popover de Fallback)
    if hasattr(st, "dialog"):
        @st.dialog("Filtros de Consulta de Vendas")
        def modal_filtros_dialog():
            render_filters_form()

        if st.sidebar.button("Configurar Filtros", use_container_width=True):
            modal_filtros_dialog()
    elif hasattr(st, "popover"):
        with st.sidebar.popover("Configurar Filtros", use_container_width=True):
            render_filters_form()
    else:
        with st.sidebar.expander("Configurar Filtros", expanded=False):
            render_filters_form()

    # Badge de status dos filtros na sidebar
    is_date_custom = st.session_state["filter_date_range"] != (min_date, max_date)
    is_prod_custom = len(st.session_state["filter_produtos"]) < len(todos_produtos)
    is_cid_custom = len(st.session_state["filter_cidades"]) < len(todas_cidades)
    is_cli_custom = len(st.session_state["filter_clientes"]) > 0
    is_cpf_custom = st.session_state["filter_cpf"] != "Todos os Registros"

    filtros_ativos = sum([is_date_custom, is_prod_custom, is_cid_custom, is_cli_custom, is_cpf_custom])

    if filtros_ativos > 0:
        st.sidebar.markdown(
            f"<div style='background:rgba(255,113,206,0.15); border:1px solid {VAPOR_PINK}; "
            f"border-radius:8px; padding:8px 12px; margin-top:12px; font-size:0.85rem; color:{VAPOR_CYAN}; text-align:center;'>"
            f"<b>{filtros_ativos} filtro(s) ativo(s)</b>"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.markdown(
            f"<div style='background:rgba(1,205,254,0.1); border:1px solid rgba(1,205,254,0.3); "
            f"border-radius:8px; padding:8px 12px; margin-top:12px; font-size:0.82rem; color:{VAPOR_TEXT_LIGHT}; text-align:center;'>"
            "Exibindo todos os registros"
            f"</div>",
            unsafe_allow_html=True,
        )

    # ==============================================================================
    # APLICAÇÃO DOS FILTROS ATIVOS NO DATAFRAME
    # ==============================================================================
    filtered_df = df.copy()

    # Validação do intervalo de datas
    active_date = st.session_state["filter_date_range"]
    if isinstance(active_date, tuple) and len(active_date) == 2:
        start_date, end_date = active_date
        filtered_df = filtered_df[
            (filtered_df["data_venda"].dt.date >= start_date) &
            (filtered_df["data_venda"].dt.date <= end_date)
        ]
    elif isinstance(active_date, tuple) and len(active_date) == 1:
        start_date = active_date[0]
        filtered_df = filtered_df[filtered_df["data_venda"].dt.date >= start_date]

    if st.session_state["filter_produtos"]:
        filtered_df = filtered_df[filtered_df["produto"].isin(st.session_state["filter_produtos"])]

    if st.session_state["filter_cidades"]:
        filtered_df = filtered_df[filtered_df["cidade"].isin(st.session_state["filter_cidades"])]

    if st.session_state["filter_clientes"]:
        filtered_df = filtered_df[filtered_df["nome_cliente"].isin(st.session_state["filter_clientes"])]

    if st.session_state["filter_cpf"] == "Apenas CPFs Válidos":
        filtered_df = filtered_df[filtered_df["cpf_valido"]]
    elif st.session_state["filter_cpf"] == "Apenas CPFs Não Informados":
        filtered_df = filtered_df[~filtered_df["cpf_valido"]]

    if filtered_df.empty:
        st.warning("Nenhuma venda localizada para os filtros selecionados. Abra o modal de filtros para ampliar a busca.")
        return

    # ==============================================================================
    # CARDS DE KPIS EXECUTIVOS COM NEON GLOW
    # ==============================================================================
    faturamento_total = filtered_df["valor_total"].sum()
    volume_total = filtered_df["quantidade"].sum()
    total_transacoes = filtered_df["id_venda"].nunique()
    ticket_medio = faturamento_total / total_transacoes if total_transacoes > 0 else 0.0
    clientes_unicos = filtered_df["nome_cliente"].nunique()

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric("Faturamento Líquido", format_currency(faturamento_total))
    with kpi2:
        st.metric("Volume Vendido", format_number(volume_total))
    with kpi3:
        st.metric("Transações Válidas", format_number(total_transacoes))
    with kpi4:
        st.metric("Ticket Médio", format_currency(ticket_medio))
    with kpi5:
        st.metric("Clientes Atendidos", format_number(clientes_unicos))

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Badges de Auditoria com brilho neon
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        st.markdown(
            f"<div style='background: rgba(35, 12, 60, 0.85); border: 1px solid rgba(255, 113, 206, 0.4); "
            f"border-radius: 10px; padding: 10px 14px; text-align: center; box-shadow: 0 0 12px rgba(255, 113, 206, 0.25);'>"
            f"<b>Carga Inicial:</b> <span style='color:{VAPOR_PINK}; font-weight:bold;'>{audit['total_registros_brutos']}</span> linhas"
            f"</div>",
            unsafe_allow_html=True,
        )
    with b2:
        st.markdown(
            f"<div style='background: rgba(35, 12, 60, 0.85); border: 1px solid rgba(1, 205, 254, 0.4); "
            f"border-radius: 10px; padding: 10px 14px; text-align: center; box-shadow: 0 0 12px rgba(1, 205, 254, 0.25);'>"
            f"<b>Duplicatas Expurgadas:</b> <span style='color:{VAPOR_CYAN}; font-weight:bold;'>{audit['duplicatas_removidas']}</span> casos"
            f"</div>",
            unsafe_allow_html=True,
        )
    with b3:
        st.markdown(
            f"<div style='background: rgba(35, 12, 60, 0.85); border: 1px solid rgba(255, 251, 150, 0.4); "
            f"border-radius: 10px; padding: 10px 14px; text-align: center; box-shadow: 0 0 12px rgba(255, 251, 150, 0.25);'>"
            f"<b>CPFs Saneados:</b> <span style='color:{VAPOR_YELLOW}; font-weight:bold;'>{audit['cpfs_ausentes_tratados']}</span> casos"
            f"</div>",
            unsafe_allow_html=True,
        )
    with b4:
        st.markdown(
            f"<div style='background: rgba(35, 12, 60, 0.85); border: 1px solid rgba(5, 255, 161, 0.4); "
            f"border-radius: 10px; padding: 10px 14px; text-align: center; box-shadow: 0 0 12px rgba(5, 255, 161, 0.25);'>"
            f"<b>Dataset Higienizado:</b> <span style='color:{VAPOR_GREEN}; font-weight:bold;'>{audit['total_registros_higienizados']}</span> vendas"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ==============================================================================
    # RENDERIZAÇÃO DA VISÃO SELECIONADA PELA SIDEBAR
    # ==============================================================================
    if aba_selecionada == "Visão Geral e Produtos":
        col_g1, col_g2 = st.columns([1.4, 1])

        with col_g1:
            st.subheader("Evolução Temporal da Receita")
            df_tempo = (
                filtered_df.groupby(["AnoMes", "produto"])["valor_total"]
                .sum()
                .reset_index()
                .sort_values(by="AnoMes")
            )
            fig_tempo = px.bar(
                df_tempo,
                x="AnoMes",
                y="valor_total",
                color="produto",
                barmode="stack",
                title="Faturamento Mensal por Produto",
                labels={"AnoMes": "Mês", "valor_total": "Receita (R$)", "produto": "Produto"},
                color_discrete_sequence=VAPOR_COLOR_SEQUENCE,
            )
            fig_tempo = apply_vaporwave_chart(fig_tempo)
            fig_tempo.update_traces(marker_line_color=VAPOR_CYAN, marker_line_width=1)
            fig_tempo.update_layout(
                xaxis_title="Mês da Venda",
                yaxis_title="Faturamento (R$)",
                margin=dict(l=10, r=10, t=40, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            )
            st.plotly_chart(fig_tempo, use_container_width=True)

        with col_g2:
            st.subheader("Participação por Categoria")
            df_prod_pie = (
                filtered_df.groupby("produto")["valor_total"]
                .sum()
                .reset_index()
                .sort_values(by="valor_total", ascending=False)
            )
            fig_pie = px.pie(
                df_prod_pie,
                names="produto",
                values="valor_total",
                hole=0.48,
                title="Distribuição do Faturamento por Produto",
                color_discrete_sequence=VAPOR_COLOR_SEQUENCE,
            )
            fig_pie = apply_vaporwave_chart(fig_pie)
            fig_pie.update_traces(
                textposition="inside",
                textinfo="percent+label",
                marker=dict(line=dict(color=VAPOR_BG, width=2)),
            )
            fig_pie.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("#### Desempenho e Volume por Produto")
        df_prod_bar = (
            filtered_df.groupby("produto")
            .agg(
                Faturamento=("valor_total", "sum"),
                Unidades=("quantidade", "sum"),
                Ticket_Medio=("valor_total", "mean"),
            )
            .reset_index()
            .sort_values(by="Faturamento", ascending=True)
        )
        fig_prod_bar = px.bar(
            df_prod_bar,
            x="Faturamento",
            y="produto",
            orientation="h",
            color="produto",
            color_discrete_sequence=VAPOR_COLOR_SEQUENCE,
            title="Receita Consolidada por Produto",
            labels={"produto": "Produto", "Faturamento": "Faturamento (R$)"},
            hover_data=["Unidades", "Ticket_Medio"],
        )
        fig_prod_bar = apply_vaporwave_chart(fig_prod_bar)
        fig_prod_bar.update_traces(
            marker_line_color=VAPOR_CYAN,
            marker_line_width=1.5,
        )
        fig_prod_bar.update_layout(
            margin=dict(l=10, r=10, t=40, b=10),
            showlegend=False,
        )
        st.plotly_chart(fig_prod_bar, use_container_width=True)

    elif aba_selecionada == "Desempenho Geográfico":
        col_geo1, col_geo2 = st.columns([1.3, 1])

        with col_geo1:
            st.subheader("Faturamento por Cidade")
            df_cidades = (
                filtered_df.groupby("cidade")
                .agg(
                    Faturamento=("valor_total", "sum"),
                    Pedidos=("id_venda", "nunique"),
                    Itens=("quantidade", "sum"),
                )
                .reset_index()
                .sort_values(by="Faturamento", ascending=False)
            )
            fig_cidades = px.bar(
                df_cidades,
                x="cidade",
                y="Faturamento",
                color="Faturamento",
                color_continuous_scale=VAPOR_CONTINUOUS_SCALE,
                title="Receita Gerada por Município",
                labels={"cidade": "Cidade", "Faturamento": "Faturamento (R$)"},
                hover_data=["Pedidos", "Itens"],
            )
            fig_cidades = apply_vaporwave_chart(fig_cidades)
            fig_cidades.update_traces(
                marker_line_color=VAPOR_PINK,
                marker_line_width=1.5,
            )
            fig_cidades.update_layout(margin=dict(l=10, r=10, t=40, b=10), xaxis_tickangle=-25)
            st.plotly_chart(fig_cidades, use_container_width=True)

        with col_geo2:
            st.subheader("Indicadores por Município")
            df_cidades["Ticket Médio"] = df_cidades["Faturamento"] / df_cidades["Pedidos"]
            st.dataframe(
                df_cidades.rename(columns={
                    "cidade": "Cidade",
                    "Faturamento": "Receita Total",
                    "Pedidos": "Transações",
                    "Itens": "Volume de Itens",
                }),
                column_config={
                    "Receita Total": st.column_config.NumberColumn("Receita Total", format="R$ %.2f"),
                    "Ticket Médio": st.column_config.NumberColumn("Ticket Médio", format="R$ %.2f"),
                    "Transações": st.column_config.NumberColumn("Transações", format="%d"),
                    "Volume de Itens": st.column_config.NumberColumn("Itens", format="%d"),
                },
                use_container_width=True,
                hide_index=True,
                height=350,
            )

    elif aba_selecionada == "Perfil dos Compradores":
        col_c1, col_c2 = st.columns([1.3, 1])

        with col_c1:
            st.subheader("Top Clientes por Volume de Compras")
            df_top_cli = (
                filtered_df.groupby(["nome_cliente", "cidade", "cpf_formatado"])
                .agg(
                    TotalGasto=("valor_total", "sum"),
                    Pedidos=("id_venda", "nunique"),
                    ItensComprados=("quantidade", "sum"),
                )
                .reset_index()
                .sort_values(by="TotalGasto", ascending=False)
            )
            fig_top_cli = px.bar(
                df_top_cli.head(10),
                x="nome_cliente",
                y="TotalGasto",
                color="cidade",
                color_discrete_sequence=VAPOR_COLOR_SEQUENCE,
                title="Top 10 Clientes por Faturamento Líquido",
                labels={"nome_cliente": "Cliente", "TotalGasto": "Total Gasto (R$)", "cidade": "Cidade"},
                hover_data=["cpf_formatado", "Pedidos", "ItensComprados"],
            )
            fig_top_cli = apply_vaporwave_chart(fig_top_cli)
            fig_top_cli.update_traces(
                marker_line_color=VAPOR_CYAN,
                marker_line_width=1.2,
            )
            fig_top_cli.update_layout(margin=dict(l=10, r=10, t=40, b=10), xaxis_tickangle=-30)
            st.plotly_chart(fig_top_cli, use_container_width=True)

        with col_c2:
            st.subheader("Sensibilidade Preço vs Quantidade")
            fig_scatter = px.scatter(
                filtered_df,
                x="valor_unitario",
                y="quantidade",
                color="produto",
                color_discrete_sequence=VAPOR_COLOR_SEQUENCE,
                size="valor_total",
                hover_name="nome_cliente",
                hover_data=["cidade", "valor_total"],
                title="Dispersão: Preço Unitário vs Volume Negociado",
                labels={"valor_unitario": "Preço Unitário (R$)", "quantidade": "Quantidade"},
            )
            fig_scatter = apply_vaporwave_chart(fig_scatter)
            fig_scatter.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_scatter, use_container_width=True)

    elif aba_selecionada == "Auditoria e Qualidade ETL":
        st.subheader("Relatório do Pipeline de Qualidade de Dados")
        st.markdown(
            "Detalhamento dos saneamentos executados pelo pipeline de ETL para assegurar conformidade "
            "com os princípios de governança e integridade analítica."
        )

        col_aud1, col_aud2 = st.columns(2)
        with col_aud1:
            st.markdown(f"<h5 style='color:{VAPOR_CYAN};'>Quadro Comparativo (Bruto vs Higienizado)</h5>", unsafe_allow_html=True)
            df_comparativo = pd.DataFrame([
                {"Métrica de Auditoria": "Registros Iniciais na Base Bruta", "Quantidade": audit["total_registros_brutos"]},
                {"Métrica de Auditoria": "Duplicatas Funcionais Descartadas", "Quantidade": audit["duplicatas_removidas"]},
                {"Métrica de Auditoria": "Registros com CPF Ausente Saneados", "Quantidade": audit["cpfs_ausentes_tratados"]},
                {"Métrica de Auditoria": "Registros Válidos no Dataset Final", "Quantidade": audit["total_registros_higienizados"]},
            ])
            st.dataframe(df_comparativo, use_container_width=True, hide_index=True)

        with col_aud2:
            st.markdown(f"<h5 style='color:{VAPOR_PINK};'>Registros Duplicados Identificados na Base Original</h5>", unsafe_allow_html=True)
            if not audit["df_duplicadas"].empty:
                st.dataframe(
                    audit["df_duplicadas"][[
                        "id_venda", "nome_cliente", "cpf", "data_venda", "produto", "quantidade", "valor_total"
                    ]],
                    use_container_width=True,
                    hide_index=True,
                    height=200,
                )
            else:
                st.info("Nenhuma duplicata localizada.")

        st.markdown("---")
        with st.expander("Exibir Base Higienizada Completa e Exportação"):
            colunas_exibir = [
                "id_venda", "data_venda", "nome_cliente", "cpf_formatado", "cidade",
                "produto", "quantidade", "valor_unitario", "valor_total"
            ]
            df_export = filtered_df[colunas_exibir].sort_values(by="data_venda", ascending=False)

            st.dataframe(
                df_export.rename(columns={"cpf_formatado": "CPF"}),
                column_config={
                    "data_venda": st.column_config.DatetimeColumn("Data Venda", format="DD/MM/YYYY"),
                    "valor_unitario": st.column_config.NumberColumn("Valor Unitário", format="R$ %.2f"),
                    "valor_total": st.column_config.NumberColumn("Valor Total", format="R$ %.2f"),
                },
                use_container_width=True,
                hide_index=True,
            )

            csv_utf8 = df_export.to_csv(index=False, sep=";").encode("utf-8-sig")
            st.download_button(
                label="Baixar Base Higienizada em UTF-8 (CSV)",
                data=csv_utf8,
                file_name="dados_vendas_higienizados_utf8.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    main()
