"""Dashboard de Análise de Vendas e Clientes.

Aplicação interativa desenvolvida em Streamlit com Plotly Express,
integrando dados transacionais de vendas (CSV) e base cadastral de clientes (Excel).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Dashboard de Vendas & Clientes | SENAI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================================
# FUNÇÕES DE CARREGAMENTO E ETL COM CACHE
# ==============================================================================
@st.cache_data
def load_and_clean_data() -> pd.DataFrame:
    """Carrega os arquivos sales_raw.csv e customers.xlsx, realiza o saneamento

    dos dados, trata valores ausentes e realiza a junção dos datasets.
    """
    base_dir = Path(__file__).parent
    sales_path = base_dir / "sales_raw.csv"
    customers_path = base_dir / "customers.xlsx"

    # Verificação de existência dos arquivos
    if not sales_path.exists() or not customers_path.exists():
        raise FileNotFoundError(
            f"Arquivos não encontrados. Certifique-se de que "
            f"'{sales_path.name}' e '{customers_path.name}' estão no diretório: {base_dir}"
        )

    # 1. Carregamento dos dados
    df_sales = pd.read_csv(sales_path)
    df_customers = pd.read_excel(customers_path, sheet_name="customers")

    # 2. Saneamento do DataFrame de Vendas
    # Conversão de data
    df_sales["date"] = pd.to_datetime(df_sales["date"], errors="coerce")

    # Tratamento de unit_price: remoção de '€', espaços e conversão
    df_sales["unit_price"] = (
        df_sales["unit_price"]
        .astype(str)
        .str.replace("€", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df_sales["unit_price"] = pd.to_numeric(df_sales["unit_price"], errors="coerce").fillna(0.0)

    # Tratamento de região: strip, title case e tratamento de nulos
    df_sales["region"] = (
        df_sales["region"]
        .fillna("Não Informada")
        .astype(str)
        .str.strip()
        .str.title()
    )

    # Tratamento de units_sold: imputação pela mediana por produto
    median_by_prod = df_sales.groupby("product")["units_sold"].transform("median")
    overall_median = df_sales["units_sold"].median()
    df_sales["units_sold"] = df_sales["units_sold"].fillna(median_by_prod).fillna(overall_median)
    df_sales["units_sold"] = df_sales["units_sold"].astype(int)

    # Cálculo da Receita Total
    df_sales["total_revenue"] = df_sales["units_sold"] * df_sales["unit_price"]

    # 3. Integração (Left Join) com a base de clientes
    merged = pd.merge(df_sales, df_customers, on="customer_id", how="left")
    merged["customer_name"] = merged["customer_name"].fillna("Cliente Desconhecido")
    merged["segment"] = merged["segment"].fillna("Não Informado")
    merged["country"] = merged["country"].fillna("Não Informado")

    return merged


def format_currency(val: float) -> str:
    """Formata valor monetário no padrão europeu com separador de milhar."""
    return f"€ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def format_number(val: int | float) -> str:
    """Formata número inteiro ou decimal com separador de milhar."""
    return f"{int(val):,}".replace(",", ".")


# ==============================================================================
# PIPELINE PRINCIPAL DA APLICAÇÃO
# ==============================================================================
def main():
    # Título e Cabeçalho
    st.title("📊 Análise de Performance de Vendas e Clientes")
    st.markdown(
        "Dashboard analítico desenvolvido com **Streamlit**, processando dados transacionais "
        "(`sales_raw.csv`) e cadastrais (`customers.xlsx`)."
    )
    st.markdown("---")

    # Tentativa de carregamento dos dados com tratamento de erro
    try:
        df = load_and_clean_data()
    except FileNotFoundError as err:
        st.error(f"⚠️ Erro ao carregar os dados: {err}")
        st.info("Verifique se os arquivos `sales_raw.csv` e `customers.xlsx` estão na mesma pasta deste script.")
        return
    except Exception as err:
        st.error(f"⚠️ Ocorreu um erro inesperado no processamento dos dados: {err}")
        return

    # ==============================================================================
    # FILTROS LATERAIS (SIDEBAR)
    # ==============================================================================
    st.sidebar.header("🔍 Filtros de Consulta")

    # 1. Filtro por Período de Data
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    date_range = st.sidebar.date_input(
        "Selecione o Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # 2. Filtro por Região
    all_regions = sorted(df["region"].unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "Região",
        options=all_regions,
        default=all_regions,
    )

    # 3. Filtro por País
    all_countries = sorted(df["country"].unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "País",
        options=all_countries,
        default=all_countries,
    )

    # 4. Filtro por Segmento do Cliente
    all_segments = sorted(df["segment"].unique().tolist())
    selected_segments = st.sidebar.multiselect(
        "Segmento de Venda",
        options=all_segments,
        default=all_segments,
    )

    # 5. Filtro por Produto
    all_products = sorted(df["product"].unique().tolist())
    selected_products = st.sidebar.multiselect(
        "Produto",
        options=all_products,
        default=all_products,
    )

    # Aplicação dos filtros dinâmicos
    filtered_df = df.copy()

    # Validação do intervalo de datas
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["date"].dt.date >= start_date) &
            (filtered_df["date"].dt.date <= end_date)
        ]
    elif isinstance(date_range, tuple) and len(date_range) == 1:
        start_date = date_range[0]
        filtered_df = filtered_df[filtered_df["date"].dt.date >= start_date]

    if selected_regions:
        filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]

    if selected_countries:
        filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

    if selected_segments:
        filtered_df = filtered_df[filtered_df["segment"].isin(selected_segments)]

    if selected_products:
        filtered_df = filtered_df[filtered_df["product"].isin(selected_products)]

    # Verificação se o filtro retornou dados
    if filtered_df.empty:
        st.warning("⚠️ Nenhum registro encontrado para a combinação de filtros selecionada.")
        return

    # ==============================================================================
    # CARDS DE MÉTRICAS (KPIS)
    # ==============================================================================
    total_revenue = filtered_df["total_revenue"].sum()
    total_units = filtered_df["units_sold"].sum()
    total_orders = filtered_df["order_id"].nunique()
    ticket_medio = total_revenue / total_orders if total_orders > 0 else 0.0
    active_customers = filtered_df["customer_id"].nunique()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("💰 Faturamento Total", format_currency(total_revenue))
    with col2:
        st.metric("📦 Unidades Vendidas", format_number(total_units))
    with col3:
        st.metric("🧾 Total de Pedidos", format_number(total_orders))
    with col4:
        st.metric("🎯 Ticket Médio", format_currency(ticket_medio))
    with col5:
        st.metric("👥 Clientes Ativos", format_number(active_customers))

    st.markdown("---")

    # ==============================================================================
    # VISUALIZAÇÕES E GRÁFICOS INTERATIVOS (PLOTLY)
    # ==============================================================================
    # Linha 1: Evolução Temporal e Desempenho por Produto
    row1_col1, row1_col2 = st.columns([1.4, 1])

    with row1_col1:
        st.subheader("📈 Evolução Temporal da Receita")
        # Agrupamento mensal para visualização mais limpa
        df_time = (
            filtered_df.set_index("date")
            .resample("ME")["total_revenue"]
            .sum()
            .reset_index()
        )
        df_time["Mês"] = df_time["date"].dt.strftime("%b/%Y")

        fig_time = px.area(
            df_time,
            x="date",
            y="total_revenue",
            labels={"date": "Data", "total_revenue": "Receita (€)"},
            title="Receita Mensal Acumulada",
            template="plotly_white",
            color_discrete_sequence=["#1E88E5"],
        )
        fig_time.update_traces(mode="lines+markers", fill="tozeroy")
        fig_time.update_layout(xaxis_title="Período", yaxis_title="Receita (€)", margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_time, width="stretch")

    with row1_col2:
        st.subheader("🏷️ Receita por Produto")
        df_prod = (
            filtered_df.groupby("product")
            .agg(Receita=("total_revenue", "sum"), Unidades=("units_sold", "sum"))
            .reset_index()
            .sort_values(by="Receita", ascending=True)
        )

        fig_prod = px.bar(
            df_prod,
            x="Receita",
            y="product",
            orientation="h",
            labels={"product": "Produto", "Receita": "Receita (€)"},
            title="Faturamento por Tipo de Produto",
            template="plotly_white",
            color="Receita",
            color_continuous_scale="Blues",
            hover_data=["Unidades"],
        )
        fig_prod.update_layout(yaxis_title=None, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_prod, width="stretch")

    # Linha 2: Distribuição Geográfica e Segmento de Venda
    row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1])

    with row2_col1:
        st.subheader("🌍 Faturamento por Região")
        df_reg = (
            filtered_df.groupby("region")["total_revenue"]
            .sum()
            .reset_index()
            .sort_values(by="total_revenue", ascending=False)
        )
        fig_reg = px.bar(
            df_reg,
            x="region",
            y="total_revenue",
            labels={"region": "Região", "total_revenue": "Receita (€)"},
            title="Distribuição por Região",
            template="plotly_white",
            color_discrete_sequence=["#43A047"],
        )
        fig_reg.update_layout(margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_reg, width="stretch")

    with row2_col2:
        st.subheader("📍 Faturamento por País")
        df_country = (
            filtered_df.groupby("country")["total_revenue"]
            .sum()
            .reset_index()
            .sort_values(by="total_revenue", ascending=False)
        )
        fig_country = px.pie(
            df_country,
            names="country",
            values="total_revenue",
            hole=0.45,
            title="Proporção por País do Cliente",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_country.update_layout(margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_country, width="stretch")

    with row2_col3:
        st.subheader("🛒 Segmento do Cliente")
        df_seg = (
            filtered_df.groupby("segment")["total_revenue"]
            .sum()
            .reset_index()
        )
        fig_seg = px.pie(
            df_seg,
            names="segment",
            values="total_revenue",
            hole=0.45,
            title="Divisão de Canais (Online vs Retail)",
            template="plotly_white",
            color_discrete_sequence=["#FF7043", "#FFA726"],
        )
        fig_seg.update_layout(margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_seg, width="stretch")

    # Linha 3: Top Clientes
    st.subheader("⭐ Top 10 Clientes por Faturamento")
    df_top_cust = (
        filtered_df.groupby(["customer_id", "customer_name", "country", "segment"])
        .agg(
            Receita_Total=("total_revenue", "sum"),
            Qtd_Pedidos=("order_id", "nunique"),
            Total_Itens=("units_sold", "sum"),
        )
        .reset_index()
        .sort_values(by="Receita_Total", ascending=False)
        .head(10)
    )

    fig_top_cust = px.bar(
        df_top_cust,
        x="customer_name",
        y="Receita_Total",
        labels={"customer_name": "Cliente", "Receita_Total": "Faturamento (€)"},
        color="segment",
        title="Maiores Compradores por Canal de Venda",
        template="plotly_white",
        hover_data=["country", "Qtd_Pedidos", "Total_Itens"],
    )
    fig_top_cust.update_layout(xaxis_title="Cliente", yaxis_title="Receita (€)", margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_top_cust, width="stretch")

    # ==============================================================================
    # TABELA DE DADOS DETALHADA E EXPORTAÇÃO
    # ==============================================================================
    with st.expander("📋 Ver Tabela de Dados Brutos Filtrados & Exportação"):
        display_cols = [
            "order_id", "date", "region", "product", "units_sold",
            "unit_price", "total_revenue", "customer_name", "segment", "country"
        ]
        st.dataframe(
            filtered_df[display_cols].sort_values(by="date", ascending=False),
            width="stretch",
            hide_index=True,
        )

        csv_data = filtered_df[display_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Baixar Dados Filtrados (CSV)",
            data=csv_data,
            file_name="dados_vendas_filtrados.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
