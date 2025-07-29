import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="ERP Dashboard",
    layout="wide"
)

API_URL = "http://localhost:8000"

def formatar_data(df, colunas_data):
    """Formata colunas de data no DataFrame"""
    for col in colunas_data:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    return df

def carregar_dados(endpoint, params=None):
    """Carrega dados da API"""
    try:
        response = requests.get(f"{API_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

def criar_grafico_vendas_categoria(dados):
    """Cria gráfico de vendas por categoria"""
    df = pd.DataFrame(dados, columns=["categoria", "total_vendas"])
    fig = px.bar(
        df,
        x="categoria",
        y="total_vendas",
        title="Vendas por Categoria",
        labels={"categoria": "Categoria", "total_vendas": "Total de Vendas (R$)"}
    )
    return fig

def criar_grafico_curva_abc(dados):
    """Cria gráfico da Curva ABC"""
    df = pd.DataFrame(dados, columns=["produto", "total_vendas"])
    df = df.sort_values("total_vendas", ascending=True)
    
    # Só vai calcular percentuais acumulados
    df["percentual"] = df["total_vendas"].cumsum() / df["total_vendas"].sum() * 100
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["produto"],
        y=df["total_vendas"],
        name="Total de Vendas"
    ))
    fig.add_trace(go.Scatter(
        x=df["produto"],
        y=df["percentual"],
        name="% Acumulado",
        yaxis="y2"
    ))
    
    fig.update_layout(
        title="Curva ABC de Produtos",
        yaxis=dict(title="Total de Vendas (R$)"),
        yaxis2=dict(title="% Acumulado", overlaying="y", side="right"),
        showlegend=True
    )
    
    return fig

def criar_grafico_margem_lucro(dados):
    """Cria gráfico de margem de lucro"""
    df = pd.DataFrame(dados, columns=["produto", "margem"])
    fig = px.bar(
        df,
        x="produto",
        y="margem",
        title="Margem de Lucro por Produto (%)",
        labels={"produto": "Produto", "margem": "Margem de Lucro (%)"}
    )
    return fig

def main():
    st.title("Dashboard de Vendas e Estoque")
    
    st.sidebar.title("Filtros")
    
    vendas_data = carregar_dados("vendas")
    if vendas_data and isinstance(vendas_data, list):
        lojas = ["Todas"] + list(set([v["loja"] for v in vendas_data if "loja" in v]))
    else:
        lojas = ["Todas"]
        st.warning("Nenhuma venda encontrada ou erro ao carregar vendas.")

    produtos_data = carregar_dados("produtos")
    if produtos_data and isinstance(produtos_data, list):
        categorias = ["Todas"] + list(set([p["categoria"] for p in produtos_data if "categoria" in p]))
    else:
        categorias = ["Todas"]
        st.warning("Nenhum produto encontrado ou erro ao carregar produtos.")
    
    loja = st.sidebar.selectbox("Loja", lojas)
    categoria = st.sidebar.selectbox("Categoria", categorias)
    
    data_inicio = st.sidebar.date_input(
        "Data Início",
        value=(datetime.now() - timedelta(days=30)).date()
    )
    data_fim = st.sidebar.date_input(
        "Data Fim",
        value=datetime.now().date()
    )
    
    # para filtrar vendas
    params = {}
    if loja != "Todas":
        params["loja"] = loja
    if categoria != "Todas":
        params["categoria"] = categoria
    params["data_inicio"] = data_inicio.isoformat()
    params["data_fim"] = data_fim.isoformat()
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de vendas por categoria
        dados_vendas_categoria = carregar_dados("analytics/vendas-categoria")
        if dados_vendas_categoria:
            fig = criar_grafico_vendas_categoria(dados_vendas_categoria)
            st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de margem de lucro
        dados_margem = carregar_dados("analytics/margem-lucro")
        if dados_margem:
            fig = criar_grafico_margem_lucro(dados_margem)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Curva ABC
        dados_curva_abc = carregar_dados("analytics/curva-abc")
        if dados_curva_abc:
            fig = criar_grafico_curva_abc(dados_curva_abc)
            st.plotly_chart(fig, use_container_width=True)
        
        # Produtos mais vendidos
        dados_mais_vendidos = carregar_dados("analytics/mais-vendidos", {"limit": 10})
        if dados_mais_vendidos:
            st.subheader("Top 10 Produtos Mais Vendidos")
            df_mais_vendidos = pd.DataFrame(dados_mais_vendidos, columns=["produto", "total_vendido"])
            st.dataframe(df_mais_vendidos, use_container_width=True)
    
    # Alerta de estoque
    st.subheader("⚠️ Alertas de Estoque")
    dados_ruptura = carregar_dados("alertas/ruptura")
    if dados_ruptura:
        df_ruptura = pd.DataFrame(dados_ruptura)
        df_ruptura = df_ruptura[df_ruptura["quantidade"] < df_ruptura["estoque_minimo"]]
        if not df_ruptura.empty:
            st.error("Produtos com estoque abaixo do mínimo!")
            st.dataframe(df_ruptura[["nome", "quantidade", "estoque_minimo"]], use_container_width=True)
        else:
            st.success("Nenhum produto com estoque crítico!")

if __name__ == "__main__":
    main()
