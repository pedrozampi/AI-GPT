"""Painel de Gestao e Auditoria de Estoque Fisico Multi-Lojas.

Aplicacao analitica interativa com arquitetura de ingestao dinamica para planilhas
Excel (.xlsx), navegacao por abas na barra lateral e modal de filtros sob demanda.
Estilizada rigorosamente sob as diretrizes do Japanese Fresh Design System (style.md).
"""

from pathlib import Path
from typing import Dict, List, Tuple, Any
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ==============================================================================
# DESIGN SYSTEM JAPANESE FRESH (TOKENS CONFORME STYLE.MD)
# ==============================================================================
# Paleta de Cores Serena e Natural
COLOR_BG_PRIMARY = "#fafaf8"       # Fundo principal (Rice White)
COLOR_BG_CARD = "#ffffff"          # Superficie dos cartoes e paineis
COLOR_BORDER = "#d4d4cf"           # Borda hairline neutra quente
COLOR_TEXT_PRIMARY = "#4a5568"     # Texto principal (Cinza Ardosia Suave)
COLOR_TEXT_SECONDARY = "#7a8a9e"   # Texto secundario (Azul Aco Suave)
COLOR_TEXT_MUTED = "#b0b8c4"       # Texto atenuado

# Acentos suaves (Pastel Japones)
ACCENT_SKY_BLUE = "#64b5f6"        # Azul Ceu primario
ACCENT_MINT_GREEN = "#98d8c8"      # Verde Menta
ACCENT_GENTLE_PINK = "#ffb7c5"     # Rosa Delicado (Alertas suaves)
ACCENT_POWDER_BLUE = "#b8d4e3"     # Azul Po

# Sequencia cromatica suave para graficos Plotly
JAPANESE_FRESH_SEQUENCE = [
    "#64b5f6",  # Sky Blue
    "#98d8c8",  # Mint Green
    "#b8d4e3",  # Powder Blue
    "#ffb7c5",  # Gentle Pink
    "#7a8a9e",  # Secondary Slate
    "#d4d4cf",  # Hairline Neutral
]

STATUS_COLOR_MAP = {
    "Normal": "#64b5f6",
    "Estoque Baixo": "#98d8c8",
    "Zerado": "#b8d4e3",
    "Ruptura / Negativo": "#ffb7c5",
}


# ==============================================================================
# CONFIGURACAO DA PAGINA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Gestao de Estoque Multi-Lojas | Painel Analitico",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================================
# INJECAO DE CSS JAPANESE FRESH (RICE WHITE, HAIRLINE, MA & ZERO SOMBRAS)
# ==============================================================================
JAPANESE_FRESH_CSS = f"""
<style>
/* 1. Base e Fundo Principal (Rice White) */
.stApp {{
    background-color: {COLOR_BG_PRIMARY} !important;
    color: {COLOR_TEXT_PRIMARY} !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    font-weight: 300 !important;
}}

/* 2. Barra Lateral Clean e Serena */
[data-testid="stSidebar"] {{
    background-color: {COLOR_BG_CARD} !important;
    border-right: 1px solid rgba(212, 212, 207, 0.4) !important;
    box-shadow: none !important;
}}

[data-testid="stSidebar"] * {{
    color: {COLOR_TEXT_PRIMARY} !important;
    font-weight: 300 !important;
}}

/* 3. Navegacao da Sidebar (Abas em Formato de Cartucho Suave) */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {{
    gap: 8px !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] label {{
    background: {COLOR_BG_PRIMARY} !important;
    border: 1px solid rgba(212, 212, 207, 0.4) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    transition: all 0.4s ease-in-out !important;
    cursor: pointer !important;
    box-shadow: none !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {{
    border-color: {ACCENT_SKY_BLUE} !important;
    background: #ffffff !important;
    transform: translateY(-1px);
}}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"],
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {{
    background: rgba(100, 181, 246, 0.12) !important;
    border-color: {ACCENT_SKY_BLUE} !important;
}}

[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] p,
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {{
    color: {COLOR_TEXT_PRIMARY} !important;
    font-weight: 400 !important;
}}

/* 4. Tipografia e Titulos Sem Caixa Alta e Sem Negrito Pesado */
h1 {{
    color: {COLOR_TEXT_PRIMARY} !important;
    font-weight: 300 !important;
    font-size: 2.1rem !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 4px !important;
}}

h2 {{
    color: {COLOR_TEXT_PRIMARY} !important;
    font-weight: 300 !important;
    font-size: 1.4rem !important;
    letter-spacing: 0.4px !important;
}}

h3 {{
    color: {COLOR_TEXT_SECONDARY} !important;
    font-weight: 300 !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.3px !important;
}}

p, span, label, div {{
    font-weight: 300 !important;
}}

/* 5. Cards de Metricas Executivas */
[data-testid="stMetric"] {{
    background-color: {COLOR_BG_CARD} !important;
    border: 1px solid rgba(212, 212, 207, 0.4) !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
    box-shadow: none !important;
    transition: all 0.4s ease-in-out !important;
}}

[data-testid="stMetric"]:hover {{
    border-color: {COLOR_BORDER} !important;
    transform: translateY(-1px);
}}

[data-testid="stMetricLabel"] {{
    color: {COLOR_TEXT_SECONDARY} !important;
    font-size: 0.82rem !important;
    font-weight: 300 !important;
    letter-spacing: 0.4px !important;
}}

[data-testid="stMetricValue"] div {{
    color: {COLOR_TEXT_PRIMARY} !important;
    font-size: 1.55rem !important;
    font-weight: 400 !important;
}}

/* 6. Botoes Principais e Secundarios */
.stButton > button, .stDownloadButton > button {{
    background-color: rgba(100, 181, 246, 0.9) !important;
    color: #ffffff !important;
    font-weight: 300 !important;
    letter-spacing: 0.5px !important;
    border-radius: 8px !important;
    border: 1px solid rgba(212, 212, 207, 0.4) !important;
    padding: 8px 20px !important;
    box-shadow: none !important;
    transition: all 0.5s ease-in-out !important;
}}

.stButton > button:hover, .stDownloadButton > button:hover {{
    background-color: {ACCENT_SKY_BLUE} !important;
    border-color: {ACCENT_POWDER_BLUE} !important;
    transform: translateY(-1px);
}}

/* 7. Divisores em Linha Ultrafina */
hr {{
    border: none !important;
    height: 1px !important;
    background-color: rgba(212, 212, 207, 0.4) !important;
    margin: 24px 0 !important;
}}

/* 8. DataFrames, Tabelas Nativas e Glide Data Grid */
[data-testid="stDataFrame"],
[data-testid="stTable"],
.stDataFrame,
div[data-testid="stDataFrame"] > div,
div[data-testid="stDataFrame"] iframe,
.dvn-scroller,
.dvn-underlay,
.gdg-canvas {{
    background-color: {COLOR_BG_CARD} !important;
    color: {COLOR_TEXT_PRIMARY} !important;
    border: 1px solid rgba(212, 212, 207, 0.4) !important;
    border-radius: 12px !important;
}}

/* 9. Container e Estrutura de Tabela Japanese Fresh (HTML Puro) */
.fresh-table-container {{
    width: 100%;
    border: 1px solid rgba(212, 212, 207, 0.4);
    border-radius: 12px;
    background-color: {COLOR_BG_CARD};
    overflow-x: auto;
    overflow-y: auto;
    margin-top: 8px;
    margin-bottom: 12px;
}}

.fresh-table {{
    width: 100%;
    border-collapse: collapse;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 0.88rem;
    color: {COLOR_TEXT_PRIMARY};
}}

.fresh-table thead th {{
    background-color: {COLOR_BG_PRIMARY} !important;
    color: {COLOR_TEXT_SECONDARY} !important;
    font-weight: 400 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.4px !important;
    padding: 12px 16px !important;
    border-bottom: 1px solid rgba(212, 212, 207, 0.4) !important;
    border-top: none !important;
    position: sticky;
    top: 0;
    z-index: 2;
}}

.fresh-table tbody tr {{
    border-bottom: 1px solid rgba(212, 212, 207, 0.22);
    transition: background-color 0.25s ease-in-out;
}}

.fresh-table tbody tr:nth-child(even) {{
    background-color: {COLOR_BG_PRIMARY};
}}

.fresh-table tbody tr:nth-child(odd) {{
    background-color: {COLOR_BG_CARD};
}}

.fresh-table tbody tr:hover {{
    background-color: rgba(100, 181, 246, 0.08) !important;
}}

.fresh-table tbody td {{
    padding: 11px 16px !important;
    color: {COLOR_TEXT_PRIMARY} !important;
    font-weight: 300 !important;
    font-size: 0.86rem !important;
}}

/* 10. Painel de Card Customizado para Ma (Espacamento Generoso) */
.fresh-card {{
    background-color: {COLOR_BG_CARD};
    border: 1px solid rgba(212, 212, 207, 0.4);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
}}
</style>
"""
st.markdown(JAPANESE_FRESH_CSS, unsafe_allow_html=True)


# ==============================================================================
# FUNCOES DE FORMATACAO AUXILIARES
# ==============================================================================
def format_currency(val: float) -> str:
    """Formata valor numerico em Real brasileiro (R$ 1.234.567,89)."""
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_number(val: int | float) -> str:
    """Formata numero inteiro com separador de milhar brasileiro."""
    return f"{int(val):,}".replace(",", ".")


def apply_japanese_fresh_theme(fig: go.Figure, height: int = 380) -> go.Figure:
    """Aplica o tema minimalista Japanese Fresh aos graficos Plotly."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            size=12,
            color=COLOR_TEXT_PRIMARY,
        ),
        margin=dict(l=30, r=30, t=50, b=30),
        height=height,
        hoverlabel=dict(
            bgcolor=COLOR_BG_CARD,
            bordercolor=COLOR_BORDER,
            font=dict(color=COLOR_TEXT_PRIMARY, size=12),
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(212, 212, 207, 0.35)",
        zerolinecolor="rgba(212, 212, 207, 0.5)",
        tickfont=dict(color=COLOR_TEXT_SECONDARY),
        title_font=dict(color=COLOR_TEXT_PRIMARY),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(212, 212, 207, 0.35)",
        zerolinecolor="rgba(212, 212, 207, 0.5)",
        tickfont=dict(color=COLOR_TEXT_SECONDARY),
        title_font=dict(color=COLOR_TEXT_PRIMARY),
    )
    return fig


def render_fresh_table(
    df: pd.DataFrame,
    max_height: int = None,
    align_right_cols: List[str] = None,
) -> None:
    """Renderiza tabela personalizada 100% aderente ao Japanese Fresh sem riscos de fundo escuro."""
    if df.empty:
        st.info("Nenhum dado localizado para exibir nesta tabela.")
        return

    align_right_cols = align_right_cols or []
    scroll_style = f"max-height: {max_height}px;" if max_height else ""

    headers_html = "".join([
        f"<th style='text-align: {'right' if col in align_right_cols else 'left'};'>{col}</th>"
        for col in df.columns
    ])

    rows_html = []
    for _, row in df.iterrows():
        cells = []
        for col in df.columns:
            val = str(row[col])
            is_right = col in align_right_cols
            # Tratamento de status com badges suaves (Japanese Fresh)
            if col in ["Classificacao", "Status", "Faixa Operacional"]:
                badge_bg = "rgba(100, 181, 246, 0.12)"
                badge_color = "#3182ce"
                if "Ruptura" in val or "Negativo" in val:
                    badge_bg = "rgba(255, 183, 197, 0.35)"
                    badge_color = "#9b2c2c"
                elif "Zerado" in val:
                    badge_bg = "rgba(184, 212, 227, 0.35)"
                    badge_color = "#2c5282"
                elif "Baixo" in val:
                    badge_bg = "rgba(152, 216, 200, 0.3)"
                    badge_color = "#234e52"
                elif "Normal" in val:
                    badge_bg = "rgba(100, 181, 246, 0.15)"
                    badge_color = "#2b6cb0"
                cell_content = f"<span style='background:{badge_bg}; color:{badge_color}; padding:3px 9px; border-radius:6px; font-size:0.78rem; font-weight:400;'>{val}</span>"
            else:
                cell_content = val

            cells.append(f"<td style='text-align: {'right' if is_right else 'left'};'>{cell_content}</td>")
        rows_html.append(f"<tr>{''.join(cells)}</tr>")

    table_html = f"""
    <div class="fresh-table-container" style="{scroll_style}">
        <table class="fresh-table">
            <thead>
                <tr>{headers_html}</tr>
            </thead>
            <tbody>
                {''.join(rows_html)}
            </tbody>
        </table>
    </div>
    """
    st.markdown(table_html, unsafe_allow_html=True)


# ==============================================================================
# INGESTAO DINAMICA & PIPELINE DE ETL COM CACHE
# ==============================================================================
@st.cache_data
def load_dynamic_inventory(sheets_folder_str: str) -> Tuple[pd.DataFrame, List[Dict[str, Any]]]:
    """Varre dinamicamente todos os arquivos .xlsx na pasta sheets/ e consolida os dados."""
    sheets_dir = Path(sheets_folder_str)
    if not sheets_dir.exists():
        return pd.DataFrame(), []

    xlsx_files = sorted(list(sheets_dir.glob("*.xlsx")))
    if not xlsx_files:
        return pd.DataFrame(), []

    all_sheets_data = []
    manifest_files = []

    category_mapping = {
        "estoque_lojas": "Geral",
        "estoque_lojas_casa_decoracao": "Casa e Decoracao",
        "estoque_lojas_eletronicos": "Eletronicos",
        "estoque_lojas_moda_acessorios": "Moda e Acessorios",
    }

    for file_path in xlsx_files:
        stem = file_path.stem.lower()
        categoria_nome = category_mapping.get(stem)
        if not categoria_nome:
            cleaned = stem.replace("estoque_lojas_", "").replace("estoque_lojas", "Geral").replace("_", " ").title()
            categoria_nome = cleaned if cleaned else "Geral"

        try:
            excel_file = pd.ExcelFile(file_path)
            total_file_rows = 0
            for sheet_name in excel_file.sheet_names:
                df_sheet = pd.read_excel(excel_file, sheet_name=sheet_name)
                df_sheet.columns = [str(c).strip().lower() for c in df_sheet.columns]
                df_sheet["categoria"] = categoria_nome
                df_sheet["arquivo_origem"] = file_path.name
                df_sheet["aba_origem"] = sheet_name
                total_file_rows += len(df_sheet)
                all_sheets_data.append(df_sheet)

            manifest_files.append({
                "arquivo": file_path.name,
                "categoria": categoria_nome,
                "abas": ", ".join(excel_file.sheet_names),
                "total_linhas": total_file_rows,
            })
        except Exception:
            continue

    if not all_sheets_data:
        return pd.DataFrame(), manifest_files

    raw_df = pd.concat(all_sheets_data, ignore_index=True)

    # 1. Deduplicacao: eliminar repeticoes exatas
    clean_df = raw_df.drop_duplicates(
        subset=["sku", "loja", "produto", "quantidade_estoque", "preco_custo", "categoria"],
        keep="first",
    ).copy()

    # 2. Padronizacao textual
    clean_df["sku"] = clean_df["sku"].astype(str).str.strip().str.upper()
    clean_df["produto"] = clean_df["produto"].astype(str).str.strip().str.title()
    clean_df["loja"] = clean_df["loja"].astype(str).str.strip().str.title()

    # 3. Tratamento de quantidade em estoque
    clean_df["quantidade_estoque"] = pd.to_numeric(clean_df["quantidade_estoque"], errors="coerce").fillna(0)
    clean_df["estoque_negativo"] = clean_df["quantidade_estoque"] < 0

    # 4. Tratamento de preco de custo
    clean_df["preco_custo"] = pd.to_numeric(clean_df["preco_custo"], errors="coerce").fillna(0.0)

    # 5. Saldo fisico seguro e Calculo do capital imobilizado
    clean_df["quantidade_fisica"] = clean_df["quantidade_estoque"].clip(lower=0)
    clean_df["valor_total_estoque"] = clean_df["quantidade_fisica"] * clean_df["preco_custo"]

    # 6. Classificacao categorica de status de estoque
    def classify_status(qty: float) -> str:
        if qty < 0:
            return "Ruptura / Negativo"
        elif qty == 0:
            return "Zerado"
        elif qty <= 5:
            return "Estoque Baixo"
        else:
            return "Normal"

    clean_df["status_estoque"] = clean_df["quantidade_estoque"].apply(classify_status)

    # 7. Padronizacao flexivel de datas
    clean_df["data_contagem"] = pd.to_datetime(
        clean_df["ultima_atualizacao"],
        dayfirst=True,
        format="mixed",
        errors="coerce",
    )
    clean_df["ultima_atualizacao_formatada"] = clean_df["data_contagem"].dt.strftime("%d/%m/%Y").fillna("Data Nao Informada")

    return clean_df, manifest_files


# ==============================================================================
# EXECUCAO PRINCIPAL DA APLICACAO
# ==============================================================================
def main() -> None:
    # Resolucao dinamica do caminho da pasta sheets/
    sheets_path = Path(__file__).parent / "sheets"

    df_clean, manifest_files = load_dynamic_inventory(str(sheets_path))

    # Tratamento de pasta ausente ou vazia
    if df_clean.empty:
        st.warning(
            f"Nenhum arquivo de planilha .xlsx foi localizado na pasta '{sheets_path.name}'. "
            "Por favor, certifique-se de depositar os arquivos de estoque para processamento automatico."
        )
        return

    # ==============================================================================
    # CABECALHO INSTITUCIONAL EXECUTIVO (SEM EMOJIS, FOCO NOS DADOS DE NEGOCIO)
    # ==============================================================================
    st.markdown("<h1>Gestao e Auditoria de Estoque Fisico Multi-Lojas</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color: #7a8a9e; font-size: 0.95rem; margin-top: -2px; margin-bottom: 20px;'>"
        "Consolidacao dinamica de inventario fisico, capital imobilizado e monitoramento de ruptura entre filiais."
        "</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='margin-top: 0; margin-bottom: 24px;'>", unsafe_allow_html=True)

    # ==============================================================================
    # ESTADO DOS FILTROS NA SESSAO
    # ==============================================================================
    todas_categorias = sorted(df_clean["categoria"].dropna().unique().tolist())
    todas_lojas = sorted(df_clean["loja"].dropna().unique().tolist())
    todos_status = ["Normal", "Estoque Baixo", "Zerado", "Ruptura / Negativo"]

    if "filter_ex4_categorias" not in st.session_state:
        st.session_state["filter_ex4_categorias"] = todas_categorias
    if "filter_ex4_lojas" not in st.session_state:
        st.session_state["filter_ex4_lojas"] = todas_lojas
    if "filter_ex4_status" not in st.session_state:
        st.session_state["filter_ex4_status"] = todos_status
    if "filter_ex4_search" not in st.session_state:
        st.session_state["filter_ex4_search"] = ""

    # ==============================================================================
    # BARRA LATERAL: NAVEGACAO POR ABAS E BOTAO DO MODAL DE FILTROS
    # ==============================================================================
    st.sidebar.markdown(
        "<h3 style='margin-top: 10px; margin-bottom: 12px; color: #4a5568;'>Navegacao</h3>",
        unsafe_allow_html=True,
    )

    view_selected = st.sidebar.radio(
        "Selecione o Modulo:",
        options=[
            "Visao Geral e Capital",
            "Auditoria de Ruptura",
            "Top SKUs em Valor",
            "Inventario Consolidado",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.sidebar.markdown("<hr style='margin: 18px 0;'>", unsafe_allow_html=True)
    st.sidebar.markdown(
        "<h3 style='margin-bottom: 10px; color: #4a5568;'>Controle de Dados</h3>",
        unsafe_allow_html=True,
    )

    # Formulario do Modal de Filtros
    def render_filter_inputs() -> None:
        st.markdown(
            "<p style='color: #7a8a9e; font-size: 0.88rem; margin-bottom: 16px;'>"
            "Selecione as dimensoes desejadas para filtrar as analises e tabelas do painel."
            "</p>",
            unsafe_allow_html=True,
        )

        f_cat = st.multiselect(
            "Categorias / Departamentos:",
            options=todas_categorias,
            default=st.session_state["filter_ex4_categorias"],
            placeholder="Selecione as categorias",
        )

        f_loj = st.multiselect(
            "Filiais / Lojas:",
            options=todas_lojas,
            default=st.session_state["filter_ex4_lojas"],
            placeholder="Selecione as lojas",
        )

        f_sta = st.multiselect(
            "Status de Estoque:",
            options=todos_status,
            default=st.session_state["filter_ex4_status"],
            placeholder="Selecione os status",
        )

        f_sea = st.text_input(
            "Busca por Produto ou SKU:",
            value=st.session_state["filter_ex4_search"],
            placeholder="Ex: Teclado, SKU-1001...",
        )

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        col_btn_apply, col_btn_reset = st.columns(2)

        with col_btn_apply:
            if st.button("Aplicar Filtros", use_container_width=True):
                st.session_state["filter_ex4_categorias"] = f_cat
                st.session_state["filter_ex4_lojas"] = f_loj
                st.session_state["filter_ex4_status"] = f_sta
                st.session_state["filter_ex4_search"] = f_sea
                st.rerun()

        with col_btn_reset:
            if st.button("Restaurar Padrao", use_container_width=True):
                st.session_state["filter_ex4_categorias"] = todas_categorias
                st.session_state["filter_ex4_lojas"] = todas_lojas
                st.session_state["filter_ex4_status"] = todos_status
                st.session_state["filter_ex4_search"] = ""
                st.rerun()

    # Disparo do Modal (ou fallback transparente)
    if hasattr(st, "dialog"):
        @st.dialog("Filtros do Inventario")
        def show_filters_modal() -> None:
            render_filter_inputs()

        if st.sidebar.button("Configurar Filtros", use_container_width=True):
            show_filters_modal()
    elif hasattr(st, "popover"):
        with st.sidebar.popover("Configurar Filtros", use_container_width=True):
            render_filter_inputs()
    else:
        with st.sidebar.expander("Configurar Filtros", expanded=False):
            render_filter_inputs()

    # Indicador de filtros ativos
    filtros_ativos_count = sum([
        len(st.session_state["filter_ex4_categorias"]) < len(todas_categorias),
        len(st.session_state["filter_ex4_lojas"]) < len(todas_lojas),
        len(st.session_state["filter_ex4_status"]) < len(todos_status),
        bool(st.session_state["filter_ex4_search"].strip()),
    ])

    if filtros_ativos_count > 0:
        st.sidebar.markdown(
            f"<div style='background: rgba(100, 181, 246, 0.08); border: 1px solid {ACCENT_SKY_BLUE}; "
            f"border-radius: 8px; padding: 8px 12px; margin-top: 10px; font-size: 0.82rem; "
            f"color: {COLOR_TEXT_PRIMARY}; text-align: center;'>"
            f"{filtros_ativos_count} dimensao(oes) filtrada(s)"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        st.sidebar.markdown(
            f"<div style='background: {COLOR_BG_PRIMARY}; border: 1px solid rgba(212, 212, 207, 0.5); "
            f"border-radius: 8px; padding: 8px 12px; margin-top: 10px; font-size: 0.82rem; "
            f"color: {COLOR_TEXT_SECONDARY}; text-align: center;'>"
            "Visualizando base integral"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Botao de Atualizacao Manual do Cache
    st.sidebar.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    if st.sidebar.button("Recarregar Planilhas", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # Informacao de planilhas processadas na sidebar
    st.sidebar.markdown("<hr style='margin: 18px 0;'>", unsafe_allow_html=True)
    st.sidebar.markdown(
        f"<p style='color: {COLOR_TEXT_MUTED}; font-size: 0.78rem; text-align: center;'>"
        f"Arquivos monitorados: {len(manifest_files)} planilhas (.xlsx)<br>"
        f"Registros consolidados: {len(df_clean)}"
        f"</p>",
        unsafe_allow_html=True,
    )

    # ==============================================================================
    # APLICACAO DOS FILTROS ATIVOS NO DATAFRAME
    # ==============================================================================
    filtered_df = df_clean.copy()

    if st.session_state["filter_ex4_categorias"]:
        filtered_df = filtered_df[filtered_df["categoria"].isin(st.session_state["filter_ex4_categorias"])]

    if st.session_state["filter_ex4_lojas"]:
        filtered_df = filtered_df[filtered_df["loja"].isin(st.session_state["filter_ex4_lojas"])]

    if st.session_state["filter_ex4_status"]:
        filtered_df = filtered_df[filtered_df["status_estoque"].isin(st.session_state["filter_ex4_status"])]

    search_query = st.session_state["filter_ex4_search"].strip().lower()
    if search_query:
        filtered_df = filtered_df[
            filtered_df["produto"].str.lower().str.contains(search_query, na=False) |
            filtered_df["sku"].str.lower().str.contains(search_query, na=False)
        ]

    if filtered_df.empty:
        st.warning("Nenhum registro localizado para os filtros selecionados. Abra o modal de filtros para ajustar a selecao.")
        return

    # ==============================================================================
    # METRICAS PRINCIPAIS EXECUTIVAS (CARDS COM ST.METRIC)
    # ==============================================================================
    total_capital = filtered_df["valor_total_estoque"].sum()
    total_volume = filtered_df["quantidade_fisica"].sum()
    total_skus = filtered_df["sku"].nunique()
    custo_medio = total_capital / total_volume if total_volume > 0 else 0.0
    total_ruptura = (filtered_df["quantidade_estoque"] <= 0).sum()
    total_planilhas = len(manifest_files)

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    with kpi1:
        st.metric("Capital Imobilizado", format_currency(total_capital))
    with kpi2:
        st.metric("Volume Fisico", format_number(total_volume))
    with kpi3:
        st.metric("SKUs Monitorados", format_number(total_skus))
    with kpi4:
        st.metric("Custo Medio Unitario", format_currency(custo_medio))
    with kpi5:
        st.metric("Itens em Ruptura / Zero", format_number(total_ruptura))
    with kpi6:
        st.metric("Planilhas Ingeridas", format_number(total_planilhas))

    st.markdown("<hr style='margin-top: 24px; margin-bottom: 28px;'>", unsafe_allow_html=True)

    # ==============================================================================
    # MODULO 1: VISAO GERAL E CAPITAL IMOBILIZADO
    # ==============================================================================
    if view_selected == "Visao Geral e Capital":
        st.markdown("<h2>Distribuicao de Capital Imobilizado</h2>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #7a8a9e; font-size: 0.9rem; margin-bottom: 24px;'>"
            "Visao agregada dos recursos financeiros aplicados em mercadorias por unidade física e departamento comercial."
            "</p>",
            unsafe_allow_html=True,
        )

        col_g1, col_g2 = st.columns([1.1, 0.9])

        with col_g1:
            st.markdown("<div class='fresh-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Capital Financeiro por Filial</h3>", unsafe_allow_html=True)
            df_loja = (
                filtered_df.groupby("loja")["valor_total_estoque"]
                .sum()
                .reset_index()
                .sort_values(by="valor_total_estoque", ascending=False)
            )

            fig_bar_loja = px.bar(
                df_loja,
                x="loja",
                y="valor_total_estoque",
                labels={"loja": "Filial", "valor_total_estoque": "Capital Imobilizado (R$)"},
                color_discrete_sequence=[ACCENT_SKY_BLUE],
                text_auto=".2s",
            )
            fig_bar_loja.update_traces(
                marker_line_color=COLOR_BORDER,
                marker_line_width=1,
                opacity=0.9,
            )
            apply_japanese_fresh_theme(fig_bar_loja, height=360)
            st.plotly_chart(fig_bar_loja, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_g2:
            st.markdown("<div class='fresh-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Participacao por Categoria</h3>", unsafe_allow_html=True)
            df_cat = (
                filtered_df.groupby("categoria")["valor_total_estoque"]
                .sum()
                .reset_index()
                .sort_values(by="valor_total_estoque", ascending=False)
            )

            fig_pie_cat = px.pie(
                df_cat,
                names="categoria",
                values="valor_total_estoque",
                hole=0.45,
                color_discrete_sequence=JAPANESE_FRESH_SEQUENCE,
            )
            fig_pie_cat.update_traces(
                textposition="inside",
                textinfo="percent+label",
                marker=dict(line=dict(color=COLOR_BG_CARD, width=1.5)),
            )
            apply_japanese_fresh_theme(fig_pie_cat, height=360)
            st.plotly_chart(fig_pie_cat, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Tabela executiva consolidada por loja
        st.markdown("<div class='fresh-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Consolidado Operacional por Unidade</h3>", unsafe_allow_html=True)

        df_summary_loja = (
            filtered_df.groupby("loja")
            .agg(
                volume_pecas=("quantidade_fisica", "sum"),
                capital_total=("valor_total_estoque", "sum"),
                skus_distintos=("sku", "nunique"),
                itens_em_ruptura=("quantidade_estoque", lambda s: (s <= 0).sum()),
            )
            .reset_index()
        )
        df_summary_loja["capital_formatado"] = df_summary_loja["capital_total"].apply(format_currency)
        df_summary_loja["volume_formatado"] = df_summary_loja["volume_pecas"].apply(format_number)
        df_summary_loja["skus_formatado"] = df_summary_loja["skus_distintos"].apply(format_number)
        df_summary_loja["ruptura_formatado"] = df_summary_loja["itens_em_ruptura"].apply(format_number)

        display_summary = df_summary_loja[
            ["loja", "skus_formatado", "volume_formatado", "capital_formatado", "ruptura_formatado"]
        ].rename(
            columns={
                "loja": "Unidade / Filial",
                "skus_formatado": "SKUs Distintos",
                "volume_formatado": "Volume em Pecas",
                "capital_formatado": "Capital Imobilizado",
                "ruptura_formatado": "Itens com Saldo <= 0",
            }
        )
        render_fresh_table(
            display_summary,
            align_right_cols=["SKUs Distintos", "Volume em Pecas", "Capital Imobilizado", "Itens com Saldo <= 0"],
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ==============================================================================
    # MODULO 2: AUDITORIA DE RUPTURA E ESTOQUE CRITICO
    # ==============================================================================
    elif view_selected == "Auditoria de Ruptura":
        st.markdown("<h2>Auditoria de Ruptura e Estoque Critico</h2>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #7a8a9e; font-size: 0.9rem; margin-bottom: 24px;'>"
            "Monitoramento de anomalias de contagem, itens esgotados e registros em faixa de ressuprimento emergencial."
            "</p>",
            unsafe_allow_html=True,
        )

        itens_negativos = (filtered_df["quantidade_estoque"] < 0).sum()
        itens_zerados = (filtered_df["quantidade_estoque"] == 0).sum()
        itens_baixos = (filtered_df["status_estoque"] == "Estoque Baixo").sum()
        itens_normais = (filtered_df["status_estoque"] == "Normal").sum()

        c_stat1, c_stat2, c_stat3, c_stat4 = st.columns(4)
        with c_stat1:
            st.metric("Ruptura Negativa (Anomalias)", format_number(itens_negativos))
        with c_stat2:
            st.metric("Saldo Zerado", format_number(itens_zerados))
        with c_stat3:
            st.metric("Estoque Baixo (1 a 5 un)", format_number(itens_baixos))
        with c_stat4:
            st.metric("Estoque Regular", format_number(itens_normais))

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

        col_aud1, col_aud2 = st.columns([1, 1])

        with col_aud1:
            st.markdown("<div class='fresh-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Distribuicao de SKUs por Status de Estoque</h3>", unsafe_allow_html=True)

            status_counts = (
                filtered_df["status_estoque"]
                .value_counts()
                .reindex(["Normal", "Estoque Baixo", "Zerado", "Ruptura / Negativo"])
                .fillna(0)
                .reset_index()
            )
            status_counts.columns = ["status", "total_skus"]

            fig_status = px.bar(
                status_counts,
                x="status",
                y="total_skus",
                color="status",
                color_discrete_map=STATUS_COLOR_MAP,
                labels={"status": "Faixa Operacional", "total_skus": "Quantidade de Registros"},
                text_auto=True,
            )
            fig_status.update_layout(showlegend=False)
            fig_status.update_traces(
                marker_line_color=COLOR_BORDER,
                marker_line_width=1,
                opacity=0.9,
            )
            apply_japanese_fresh_theme(fig_status, height=340)
            st.plotly_chart(fig_status, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_aud2:
            st.markdown("<div class='fresh-card'>", unsafe_allow_html=True)
            st.markdown("<h3>Itens Criticos por Filial</h3>", unsafe_allow_html=True)
            df_criticos_loja = (
                filtered_df[filtered_df["quantidade_estoque"] <= 5]
                .groupby(["loja", "status_estoque"])
                .size()
                .reset_index(name="quantidade")
            )

            fig_crit_loja = px.bar(
                df_criticos_loja,
                x="loja",
                y="quantidade",
                color="status_estoque",
                color_discrete_map=STATUS_COLOR_MAP,
                barmode="group",
                labels={"loja": "Filial", "quantidade": "Itens Criticos", "status_estoque": "Status"},
            )
            fig_crit_loja.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    font=dict(size=11),
                )
            )
            apply_japanese_fresh_theme(fig_crit_loja, height=340)
            st.plotly_chart(fig_crit_loja, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Relacao de Itens Criticos para Reposicao
        st.markdown("<div class='fresh-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Relação Detalhada de Produtos em Ruptura ou Risco</h3>", unsafe_allow_html=True)

        df_alertas = filtered_df[filtered_df["quantidade_estoque"] <= 5].copy()
        df_alertas = df_alertas.sort_values(by=["quantidade_estoque", "valor_total_estoque"], ascending=[True, False])

        if df_alertas.empty:
            st.info("Nenhum item em estado crítico ou de ruptura com os filtros aplicados.")
        else:
            df_alertas_disp = df_alertas[
                [
                    "sku",
                    "produto",
                    "categoria",
                    "loja",
                    "quantidade_estoque",
                    "status_estoque",
                    "preco_custo",
                    "ultima_atualizacao_formatada",
                ]
            ].copy()

            df_alertas_disp["preco_custo"] = df_alertas_disp["preco_custo"].apply(format_currency)
            df_alertas_disp = df_alertas_disp.rename(
                columns={
                    "sku": "SKU",
                    "produto": "Produto",
                    "categoria": "Categoria",
                    "loja": "Filial",
                    "quantidade_estoque": "Saldo Estoque",
                    "status_estoque": "Classificacao",
                    "preco_custo": "Custo Unitario",
                    "ultima_atualizacao_formatada": "Ultima Contagem",
                }
            )
            render_fresh_table(
                df_alertas_disp,
                max_height=420,
                align_right_cols=["Saldo Estoque", "Custo Unitario"],
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # ==============================================================================
    # MODULO 3: TOP SKUS EM VALOR
    # ==============================================================================
    elif view_selected == "Top SKUs em Valor":
        st.markdown("<h2>Curva ABC e Ranking de Capital por Produto</h2>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #7a8a9e; font-size: 0.9rem; margin-bottom: 24px;'>"
            "Identificacao dos produtos que concentram maior capital financeiro imobilizado no estoque ativo."
            "</p>",
            unsafe_allow_html=True,
        )

        col_sel, col_empty = st.columns([0.3, 0.7])
        with col_sel:
            top_n = st.selectbox("Quantidade de SKUs em Destaque:", options=[10, 15, 20, 30], index=0)

        df_sku_val = (
            filtered_df.groupby(["sku", "produto", "categoria"])
            .agg(
                capital_total=("valor_total_estoque", "sum"),
                volume_pecas=("quantidade_fisica", "sum"),
                preco_medio=("preco_custo", "mean"),
            )
            .reset_index()
            .sort_values(by="capital_total", ascending=False)
        )

        top_df = df_sku_val.head(top_n).copy()
        top_df["label_completo"] = top_df["sku"] + " - " + top_df["produto"]

        st.markdown("<div class='fresh-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3>Top {top_n} SKUs por Capital Imobilizado</h3>", unsafe_allow_html=True)

        fig_top = px.bar(
            top_df.sort_values(by="capital_total", ascending=True),
            x="capital_total",
            y="label_completo",
            orientation="h",
            color_discrete_sequence=[ACCENT_MINT_GREEN],
            labels={"capital_total": "Capital Imobilizado (R$)", "label_completo": "Produto (SKU)"},
            text_auto=".2s",
        )
        fig_top.update_traces(
            marker_line_color=COLOR_BORDER,
            marker_line_width=1,
            opacity=0.9,
        )
        apply_japanese_fresh_theme(fig_top, height=max(380, top_n * 28))
        st.plotly_chart(fig_top, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Concentracao financeira
        capital_top = top_df["capital_total"].sum()
        pct_concentracao = (capital_top / total_capital * 100) if total_capital > 0 else 0.0

        st.markdown(
            f"<div style='background: {COLOR_BG_CARD}; border: 1px solid rgba(212, 212, 207, 0.4); "
            f"border-radius: 12px; padding: 18px 24px; margin-bottom: 24px;'>"
            f"<p style='color: {COLOR_TEXT_PRIMARY}; font-size: 0.95rem; margin: 0;'>"
            f"Os <b>{top_n} principais SKUs</b> concentram <b>{format_currency(capital_top)}</b>, "
            f"o que representa <b>{pct_concentracao:.1f}%</b> de todo o capital imobilizado filtrado."
            f"</p></div>",
            unsafe_allow_html=True,
        )

        # Tabela dos top SKUs
        st.markdown("<div class='fresh-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Detalhamento dos Produtos Lideres</h3>", unsafe_allow_html=True)

        top_df_disp = top_df[["sku", "produto", "categoria", "volume_pecas", "preco_medio", "capital_total"]].copy()
        top_df_disp["volume_pecas"] = top_df_disp["volume_pecas"].apply(format_number)
        top_df_disp["preco_medio"] = top_df_disp["preco_medio"].apply(format_currency)
        top_df_disp["capital_total"] = top_df_disp["capital_total"].apply(format_currency)

        top_df_disp = top_df_disp.rename(
            columns={
                "sku": "SKU",
                "produto": "Descricao do Item",
                "categoria": "Departamento",
                "volume_pecas": "Volume Fisico (un)",
                "preco_medio": "Preco Custo Medio",
                "capital_total": "Capital Imobilizado",
            }
        )
        render_fresh_table(
            top_df_disp,
            align_right_cols=["Volume Fisico (un)", "Preco Custo Medio", "Capital Imobilizado"],
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ==============================================================================
    # MODULO 4: INVENTARIO CONSOLIDADO E EXPORTACAO
    # ==============================================================================
    elif view_selected == "Inventario Consolidado":
        st.markdown("<h2>Inventario Fisico Consolidado e Exportacao</h2>", unsafe_allow_html=True)
        st.markdown(
            "<p style='color: #7a8a9e; font-size: 0.9rem; margin-bottom: 24px;'>"
            "Visao completa dos registros integrados de todas as planilhas e abas com opcao de download em formato CSV."
            "</p>",
            unsafe_allow_html=True,
        )

        # Resumo dos arquivos ingeridos
        st.markdown("<div class='fresh-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Origem dos Dados e Planilhas Ingeridas Dinamicamente</h3>", unsafe_allow_html=True)

        df_manifest = pd.DataFrame(manifest_files).rename(
            columns={
                "arquivo": "Arquivo Fonte (.xlsx)",
                "categoria": "Departamento Atribuido",
                "abas": "Abas Processadas",
                "total_linhas": "Linhas Brutas",
            }
        )
        render_fresh_table(
            df_manifest,
            align_right_cols=["Linhas Brutas"],
        )
        st.markdown("</div>", unsafe_allow_html=True)

        # Tabela consolidada com opcao de download
        st.markdown("<div class='fresh-card'>", unsafe_allow_html=True)
        st.markdown("<h3>Base de Dados Saneada e Auditada</h3>", unsafe_allow_html=True)

        df_export = filtered_df[
            [
                "sku",
                "produto",
                "categoria",
                "loja",
                "quantidade_estoque",
                "status_estoque",
                "preco_custo",
                "valor_total_estoque",
                "ultima_atualizacao_formatada",
                "arquivo_origem",
            ]
        ].copy()

        df_export_disp = df_export.copy()
        df_export_disp["preco_custo"] = df_export_disp["preco_custo"].apply(format_currency)
        df_export_disp["valor_total_estoque"] = df_export_disp["valor_total_estoque"].apply(format_currency)
        df_export_disp = df_export_disp.rename(
            columns={
                "sku": "SKU",
                "produto": "Produto",
                "categoria": "Categoria",
                "loja": "Filial",
                "quantidade_estoque": "Estoque Fisico",
                "status_estoque": "Status",
                "preco_custo": "Custo Unitario",
                "valor_total_estoque": "Capital Total",
                "ultima_atualizacao_formatada": "Ultima Contagem",
                "arquivo_origem": "Arquivo de Origem",
            }
        )

        render_fresh_table(
            df_export_disp,
            max_height=480,
            align_right_cols=["Estoque Fisico", "Custo Unitario", "Capital Total"],
        )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        csv_data = df_export.to_csv(index=False, sep=";", encoding="utf-8-sig")
        st.download_button(
            label="Baixar Base Consolidada em CSV",
            data=csv_data,
            file_name="estoque_multi_lojas_consolidado.csv",
            mime="text/csv",
        )
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
