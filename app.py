
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

import requests
import io

# ID do seu arquivo no Google Drive
file_id = "1FjxGVrbKsvLyXLL1H2wV-snEf0OCaZnZ"  # <-- substitua pelo seu ID real
download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

st.info("🔄 Buscando planilha do Google Drive...")

try:
    response = requests.get(download_url)
    file = io.BytesIO(response.content)
    df = pd.read_excel(file)

    st.success("✅ Dados carregados com sucesso do Google Drive!")

except Exception as e:
    st.error("Erro ao carregar arquivo do Google Drive:")
    st.exception(e)

st.title("📊 Painel de Cargas - Uranttia Transportes")


if st.button("🔄 Recarregar painel"):
    st.rerun()
    



# WIDGETS N.1

# Cria quatro colunas lado a lado
col1, col2, col3, col4 = st.columns(4)

# Widget 1: Total da coluna "Saída" (coluna E ou índice 4)
with col1:
    try:
        valor_total_saida = df["Saída"].sum()
        st.metric(label="💸 Total de Saídas", value=f"R$ {valor_total_saida:,.2f}")
    except:
        valor_total_saida = 0
        st.warning("❌ Coluna 'Saída' não encontrada.")

# Widget 2: Total da coluna "Mendonça" (coluna F ou índice 5)
with col2:
    try:
        valor_mendonca = df["Mendonça"].sum()
        st.metric(label="🚚 Total Mendonça", value=f"R$ {valor_mendonca:,.2f}")
    except:
        valor_mendonca = 0
        st.warning("❌ Coluna 'Mendonça' não encontrada.")

# Widget 3: Total da coluna "Entrada" (coluna G ou índice 6)
with col3:
    try:
        valor_entrada = df["Entrada"].sum()
        st.metric(label="🏦 Total de Entradas", value=f"R$ {valor_entrada:,.2f}")
    except:
        valor_entrada = 0
        st.warning("❌ Coluna 'Entrada' não encontrada.")

# Widget 4: Lucro = Entrada + Saída + Mendonça
with col4:
    lucro = valor_entrada + valor_total_saida + valor_mendonca
    st.metric(label="💰 Lucro", value=f"R$ {lucro:,.2f}")






# WIDGETS N.2

st.subheader("📆 Valores do Mês Atual")

# Certifique-se que a coluna "Data" está em datetime
df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

# Filtra o DataFrame para o mês atual
mes_atual = pd.Timestamp.now().month
ano_atual = pd.Timestamp.now().year
df_mes = df[(df['Data'].dt.month == mes_atual) & (df['Data'].dt.year == ano_atual)]

# Cria colunas para os widgets do mês atual
col1, col2, col3, col4 = st.columns(4)

# Saída (mês atual)
with col1:
    try:
        saida_mes = df_mes["Saída"].sum()
        st.metric(label="💸 Saídas (mês atual)", value=f"R$ {saida_mes:,.2f}")
    except:
        saida_mes = 0
        st.warning("❌ Coluna 'Saída' não encontrada.")

# Mendonça (mês atual)
with col2:
    try:
        mendonca_mes = df_mes["Mendonça"].sum()
        st.metric(label="🚚 Mendonça (mês atual)", value=f"R$ {mendonca_mes:,.2f}")
    except:
        mendonca_mes = 0
        st.warning("❌ Coluna 'Mendonça' não encontrada.")

# Entrada (mês atual)
with col3:
    try:
        entrada_mes = df_mes["Entrada"].sum()
        st.metric(label="🏦 Entradas (mês atual)", value=f"R$ {entrada_mes:,.2f}")
    except:
        entrada_mes = 0
        st.warning("❌ Coluna 'Entrada' não encontrada.")

# Widget 4: Lucro (mês atual) = Entrada + Saída + Mendonça
with col4:
    lucro_mes = entrada_mes + saida_mes + mendonca_mes
    st.metric(label="💰 Lucro (mês atual)", value=f"R$ {lucro_mes:,.2f}")






# GRAFICO COMPARATIVO

st.subheader("📈 Evolução no Mês Atual (com Lucro)")

# Garante que a coluna "Data" está em datetime
df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

# Filtra para o mês atual
mes_atual = pd.Timestamp.now().month
ano_atual = pd.Timestamp.now().year
df_mes = df[(df['Data'].dt.month == mes_atual) & (df['Data'].dt.year == ano_atual)]

# Agrupa por data e calcula valores
df_grouped = df_mes.groupby('Data')[['Entrada', 'Saída', 'Mendonça']].sum().reset_index()

# Calcula Lucro = Entrada + Saída + Mendonça
df_grouped['Lucro'] = df_grouped['Entrada'] + df_grouped['Saída'] + df_grouped['Mendonça']

# Gráfico
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(14, 6))

# Linhas
ax.plot(df_grouped['Data'], df_grouped['Entrada'], label='🏦 Entrada', marker='o')
ax.plot(df_grouped['Data'], df_grouped['Saída'], label='💸 Saída', marker='o')
ax.plot(df_grouped['Data'], df_grouped['Mendonça'], label='🚚 Mendonça', marker='o')
ax.plot(df_grouped['Data'], df_grouped['Lucro'], label='💰 Lucro', marker='o', linestyle='--', linewidth=2)

# Rótulos de dados
for i in range(len(df_grouped)):
    ax.text(df_grouped['Data'][i], df_grouped['Entrada'][i], f"R$ {df_grouped['Entrada'][i]:,.0f}", ha='center', va='bottom', fontsize=8)
    ax.text(df_grouped['Data'][i], df_grouped['Saída'][i],   f"R$ {df_grouped['Saída'][i]:,.0f}", ha='center', va='bottom', fontsize=8)
    ax.text(df_grouped['Data'][i], df_grouped['Mendonça'][i],f"R$ {df_grouped['Mendonça'][i]:,.0f}", ha='center', va='bottom', fontsize=8)
    ax.text(df_grouped['Data'][i], df_grouped['Lucro'][i],   f"R$ {df_grouped['Lucro'][i]:,.0f}", ha='center', va='bottom', fontsize=8, color='green')

# Estética do gráfico
ax.set_title("Evolução de Entradas, Saídas, Mendonça e Lucro - Mês Atual")
ax.set_xlabel("Data")
ax.set_ylabel("Valor (R$)")
ax.legend()
ax.grid(True)

st.pyplot(fig)










# GRÁFICO HISTÓRICO

st.subheader("📊 Evolução Histórica Mensal (Ordenado e Sem Duplicação)")

# Garantir data válida
df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

# Preenche nulos
df[['Entrada', 'Saída', 'Mendonça']] = df[['Entrada', 'Saída', 'Mendonça']].fillna(0)

# Calcula lucro
df['Lucro'] = df['Entrada'] + df['Saída'] + df['Mendonça']

# Força a data para o primeiro dia do mês (normalização)
df['AnoMes'] = df['Data'].values.astype('datetime64[M]')

# Agrupa por mês
df_mensal = df.groupby('AnoMes')[['Entrada', 'Saída', 'Mendonça', 'Lucro']].sum().reset_index()

# Gráfico
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

fig, ax = plt.subplots(figsize=(14, 6))

x = df_mensal['AnoMes']

ax.plot(x, df_mensal['Entrada'], label='🏦 Entrada', marker='o')
ax.plot(x, df_mensal['Saída'], label='💸 Saída', marker='o')
ax.plot(x, df_mensal['Mendonça'], label='🚚 Mendonça', marker='o')
ax.plot(x, df_mensal['Lucro'], label='💰 Lucro', marker='o', linestyle='--', linewidth=2)

# Rótulos com R$
for i in range(len(df_mensal)):
    ax.text(x[i], df_mensal['Entrada'][i], f"R$ {df_mensal['Entrada'][i]:,.0f}", ha='center', va='bottom', fontsize=8)
    ax.text(x[i], df_mensal['Saída'][i], f"R$ {df_mensal['Saída'][i]:,.0f}", ha='center', va='bottom', fontsize=8)
    ax.text(x[i], df_mensal['Mendonça'][i], f"R$ {df_mensal['Mendonça'][i]:,.0f}", ha='center', va='bottom', fontsize=8)
    ax.text(x[i], df_mensal['Lucro'][i], f"R$ {df_mensal['Lucro'][i]:,.0f}", ha='center', va='bottom', fontsize=8, color='green')

# Eixo X formatado corretamente
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
fig.autofmt_xdate(rotation=45)

ax.set_title("Evolução Mensal de Entradas, Saídas, Mendonça e Lucro")
ax.set_xlabel("Mês")
ax.set_ylabel("Valor (R$)")
ax.grid(True)
ax.legend()

st.pyplot(fig)















# GRÁFICO FLUXO DE LUCRO
# Filtra apenas o mês atual
# Garante data correta
df['Data'] = pd.to_datetime(df['Data'], errors='coerce')

# Preenche nulos com zero (para evitar erros no cálculo)
df[['Entrada', 'Saída', 'Mendonça']] = df[['Entrada', 'Saída', 'Mendonça']].fillna(0)

# Calcula a coluna "Lucro"
df['Lucro'] = df['Entrada'] + df['Saída'] + df['Mendonça']

# Filtra apenas o mês atual
mes_atual = pd.Timestamp.now().month
ano_atual = pd.Timestamp.now().year
df_mes_atual = df[(df['Data'].dt.month == mes_atual) & (df['Data'].dt.year == ano_atual)]

# Verifica se há dados
if not df_mes_atual.empty and 'Lucro' in df_mes_atual.columns:
    st.subheader("📈 Gráfico de Barras - Lucro por Lançamento (Mês Atual)")

    fig, ax = plt.subplots(figsize=(14, 6))
    lucro_values = df_mes_atual['Lucro']
    ax.bar(range(len(lucro_values)), lucro_values, color='green')

    # Rótulos no topo
    for i, val in enumerate(lucro_values):
        ax.text(i, val, f'R$ {val:,.0f}', ha='center', va='bottom', fontsize=8)

    ax.set_xlabel("Lançamento")
    ax.set_ylabel("Lucro (R$)")
    ax.set_title("Lucro por Lançamento - Somente Mês Atual")
    st.pyplot(fig)
else:
    st.warning("Nenhum dado de lucro disponível para o mês atual.")






# TABELA

st.subheader("📒 Tabela Geral de Lançamentos (Todos os Meses)")

# Prepara todos os dados (sem filtro por mês)
df_geral = df[['Descrição', 'Tipo', 'Data', 'Entrada', 'Saída', 'Mendonça']].copy()

# Garante que a coluna Data esteja em datetime
df_geral['Data'] = pd.to_datetime(df_geral['Data'], errors='coerce')

# Calcula Lucro
df_geral['Lucro'] = df_geral['Entrada'] + df_geral['Saída'] + df_geral['Mendonça']

# Reorganiza colunas
df_geral = df_geral[['Descrição', 'Tipo', 'Data', 'Entrada', 'Saída', 'Mendonça', 'Lucro']]

# Aplica formatação condicional por sinal (positivo/negativo)
def cor_por_valor(val):
    if isinstance(val, (int, float)):
        return 'color: green;' if val > 0 else 'color: red;'
    return ''

# Estiliza a tabela
styled_geral = (
    df_geral.style
    .format({
        'Entrada': 'R$ {:,.2f}',
        'Saída': 'R$ {:,.2f}',
        'Mendonça': 'R$ {:,.2f}',
        'Lucro': 'R$ {:,.2f}',
    })
    .applymap(cor_por_valor, subset=['Entrada', 'Saída', 'Mendonça', 'Lucro'])
)

# Exibe no painel
st.dataframe(styled_geral, use_container_width=True)







# Botão para recarregar (opcional)
if st.button("🔄 Recarregar"):
    st.experimental_rerun()


