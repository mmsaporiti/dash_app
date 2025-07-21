import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(layout="wide")

# Define os segmentos e ações
segmentos = {
    "Bancos": {
        "BBAS3.SA": "Banco do Brasil",
        "ITUB4.SA": "Itaú Unibanco",
        "BBDC4.SA": "Bradesco",
        "SANB11.SA": "Santander"
    },
    "Energia": {
        "TAEE11.SA": "Taesa",
        "CMIG4.SA": "Cemig",
        "ELET3.SA": "Eletrobras"
    },
    "Varejo": {
        "MGLU3.SA": "Magazine Luiza",
        "VIIA3.SA": "Via",
        "PETZ3.SA": "Petz"
    }
}

# Sidebar
st.sidebar.header("🔎 Filtros")

segmento = st.sidebar.selectbox("Escolha um segmento", list(segmentos.keys()))
periodo_opcao = st.sidebar.selectbox("Período", ["5y", "max"], format_func=lambda x: "5 anos" if x == "5y" else "Máx")

# Ações do segmento selecionado
acoes = segmentos[segmento]
codigos = list(acoes.keys())

# Download dos dados
@st.cache_data(ttl=60 * 5)
def baixar_dados(tickers, periodo):
    return yf.download(tickers, period=periodo, interval="1d", progress=False, group_by='ticker')

dados = baixar_dados(codigos, periodo_opcao)

st.title(f"📈 Ações do segmento: {segmento}")

# Gráficos
for codigo, nome in acoes.items():
    df = dados[codigo].dropna()
    if df.empty:
        continue

    preco_atual = df["Close"][-1]
    preco_inicial = df["Close"].iloc[0]
    variacao = ((preco_atual - preco_inicial) / preco_inicial) * 100

    col = st.container()
    with col:
        # Card
        st.metric(
            label=f"💼 {codigo} - {nome}",
            value=f"R$ {preco_atual:.2f}",
            delta=f"{variacao:.2f}%",
            delta_color="normal" if variacao == 0 else ("inverse" if variacao < 0 else "normal")
        )

        # Gráfico
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Fechamento"))
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=250,
            xaxis_title=None,
            yaxis_title=None,
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
