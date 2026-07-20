import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Financeiro", layout="wide")
st.title("📊 Dashboard de Finanças Pessoais")
st.markdown("---")

# Dados direto no código para não dar erro de arquivo sumido
dados = {
    "Data": ["2026-01-02", "2026-01-03", "2026-01-05", "2026-01-10", "2026-01-15"],
    "Categoria": ["Alimentação", "Salário", "Transporte", "Moradia", "Lazer"],
    "Tipo": ["Despesa", "Receita", "Despesa", "Despesa", "Despesa"],
    "Valor": [55.30, 5000.00, 40.00, 1200.00, 150.00]
}
df = pd.DataFrame(dados)

receitas = df[df["Tipo"] == "Receita"]["Valor"].sum()
despesas = df[df["Tipo"] == "Despesa"]["Valor"].sum()
saldo_atual = receitas - despesas

col1, col2, col3 = st.columns(3)
col1.metric(label="Total de Receitas", value=f"R$ {receitas:,.2f}")
col2.metric(label="Total de Despesas", value=f"R$ {despesas:,.2f}")
col3.metric(label="Saldo Atual", value=f"R$ {saldo_atual:,.2f}")

st.markdown("---")
st.subheader("💡 Onde você está gastando mais?")
df_despesas = df[df["Tipo"] == "Despesa"]
fig = px.pie(df_despesas, values="Valor", names="Categoria", title="Distribuição das Despesas")
st.plotly_chart(fig)