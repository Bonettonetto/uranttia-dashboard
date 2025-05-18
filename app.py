
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

st.set_page_config(layout="wide")
st.title("🚛 Painel de Cargas - Uranttia Transportes")

# Upload do Excel (para produção, substituir por leitura do Google Drive se desejar)
uploaded_file = st.file_uploader("📂 Envie o arquivo Excel", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Garantir tipos corretos
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    df[['Entrada', 'Saída', 'Mendonça']] = df[['Entrada', 'Saída', 'Mendonça']].fillna(0)
    df['Lucro'] = df['Entrada'] + df['Saída'] + df['Mendonça']

    st.markdown("### 🔢 Dados Brutos")
    st.dataframe(df, use_container_width=True)

    # 🔢 KPIs Totais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💸 Total Saída", f"R$ {df['Saída'].sum():,.2f}")
    with col2:
        st.metric("🚚 Total Mendonça", f"R$ {df['Mendonça'].sum():,.2f}")
    with col3:
        st.metric("🏦 Total Entrada", f"R$ {df['Entrada'].sum():,.2f}")
    with col4:
        st.metric("💰 Lucro Total", f"R$ {df['Lucro'].sum():,.2f}")

    # KPIs do mês atual
    mes_atual = pd.Timestamp.now().month
    ano_atual = pd.Timestamp.now().year
    df_mes = df[(df['Data'].dt.month == mes_atual) & (df['Data'].dt.year == ano_atual)]

    st.subheader("📆 Indicadores do Mês Atual")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💸 Saída (Mês)", f"R$ {df_mes['Saída'].sum():,.2f}")
    with col2:
        st.metric("🚚 Mendonça (Mês)", f"R$ {df_mes['Mendonça'].sum():,.2f}")
    with col3:
        st.metric("🏦 Entrada (Mês)", f"R$ {df_mes['Entrada'].sum():,.2f}")
    with col4:
        lucro_mes = df_mes['Entrada'].sum() + df_mes['Saída'].sum() + df_mes['Mendonça'].sum()
        st.metric("💰 Lucro (Mês)", f"R$ {lucro_mes:,.2f}")

    # 📈 Gráfico de barras - Lucro por lançamento (mês atual)
    if not df_mes.empty:
        st.subheader("📊 Lucro por Lançamento - Mês Atual")
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.bar(range(len(df_mes)), df_mes['Lucro'], color='green')
        for i, val in enumerate(df_mes['Lucro']):
            ax.text(i, val, f'R$ {val:,.0f}', ha='center', va='bottom', fontsize=8)
        ax.set_xlabel("Lançamento")
        ax.set_ylabel("Lucro (R$)")
        ax.set_title("Lucro por Lançamento (Mês Atual)")
        st.pyplot(fig)

    # 📊 Evolução Histórica Mensal
    st.subheader("📈 Evolução Histórica Mensal")

    df['AnoMes'] = df['Data'].values.astype('datetime64[M]')
    df_mensal = df.groupby('AnoMes')[['Entrada', 'Saída', 'Mendonça', 'Lucro']].sum().reset_index()

    fig, ax = plt.subplots(figsize=(14, 6))
    x = df_mensal['AnoMes']
    ax.plot(x, df_mensal['Entrada'], label='🏦 Entrada', marker='o')
    ax.plot(x, df_mensal['Saída'], label='💸 Saída', marker='o')
    ax.plot(x, df_mensal['Mendonça'], label='🚚 Mendonça', marker='o')
    ax.plot(x, df_mensal['Lucro'], label='💰 Lucro', marker='o', linestyle='--', linewidth=2)

    for i in range(len(df_mensal)):
        ax.text(x[i], df_mensal['Entrada'][i], f"R$ {df_mensal['Entrada'][i]:,.0f}", ha='center', va='bottom', fontsize=8)
        ax.text(x[i], df_mensal['Saída'][i], f"R$ {df_mensal['Saída'][i]:,.0f}", ha='center', va='bottom', fontsize=8)
        ax.text(x[i], df_mensal['Mendonça'][i], f"R$ {df_mensal['Mendonça'][i]:,.0f}", ha='center', va='bottom', fontsize=8)
        ax.text(x[i], df_mensal['Lucro'][i], f"R$ {df_mensal['Lucro'][i]:,.0f}", ha='center', va='bottom', fontsize=8, color='green')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    fig.autofmt_xdate(rotation=45)
    ax.set_title("Evolução Mensal de Entradas, Saídas, Mendonça e Lucro")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Valor (R$)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

else:
    st.info("Por favor, envie o arquivo Excel para visualizar os dados.")
