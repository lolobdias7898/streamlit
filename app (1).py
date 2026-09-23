import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# CONFIGURAÇÃO
# ==========================================

st.set_page_config(
    page_title="Dashboard de Dados",
    layout="wide"
)

st.title("Dashboard de Dados")


# ==========================================
# LEITURA DO ARQUIVO
# ==========================================

df = pd.read_csv(
    "capacidade-instalada-geracao-uf.csv",
    encoding="latin-1", sep=";"
)

# Remover espaços dos nomes das colunas
df.columns = df.columns.str.strip()


# ==========================================
# IDENTIFICAR COLUNA DE POTÊNCIA
# ==========================================

coluna_potencia = None

for coluna in df.columns:
    nome = coluna.lower().replace(" ", "")

    if "potencia" in nome or "potência" in nome:
        coluna_potencia = coluna
        break

if coluna_potencia is None:
    st.error("Não foi encontrada a coluna de potência no arquivo.")

    st.write("Colunas encontradas:")
    st.write(df.columns.tolist())

    st.stop()


# Converter potência para número
df[coluna_potencia] = pd.to_numeric(
    df[coluna_potencia]
    .astype(str)
    .str.replace(",", ".", regex=False),
    errors="coerce"
)


# ==========================================
# VISUALIZAÇÃO DOS DADOS
# ==========================================

st.subheader("Visualização dos dados")

st.dataframe(df.head())


# ==========================================
# QUANTIDADE DE REGISTROS E COLUNAS
# ==========================================

col1, col2 = st.columns(2)

col1.metric(
    "Quantidade de registros",
    df.shape[0]
)

col2.metric(
    "Quantidade de colunas",
    df.shape[1]
)


# ==========================================
# VERIFICAÇÃO DOS DADOS
# ==========================================

st.subheader("Verificação dos dados")

st.write("Valores ausentes:")
st.write(df.isnull().sum())

st.write("Quantidade de linhas duplicadas:")
st.write(df.duplicated().sum())

st.write("Tipos de dados:")
st.write(df.dtypes)


# ==========================================
# MAIOR POTÊNCIA
# ==========================================

df_validos = df.dropna(subset=[coluna_potencia])

if not df_validos.empty:

    maior = df_validos.loc[
        df_validos[coluna_potencia].idxmax()
    ]

    st.subheader("Estado com maior potência instalada")

    st.write(
        maior["NomUF"],
        maior[coluna_potencia],
        "kW"
    )


# ==========================================
# MENOR POTÊNCIA
# ==========================================

if not df_validos.empty:

    menor = df_validos.loc[
        df_validos[coluna_potencia].idxmin()
    ]

    st.subheader("Estado com menor potência instalada")

    st.write(
        menor["NomUF"],
        menor[coluna_potencia],
        "kW"
    )


# ==========================================
# GRÁFICO POR ESTADO
# ==========================================

fig = px.bar(
    df,
    x="NomUF",
    y=coluna_potencia,
    title="Potência instalada por estado"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.markdown("""
### O que podemos observar?

Os dados mostram a potência instalada registrada em cada estado.

É possível comparar os estados e identificar quais apresentam maiores e
menores valores de potência instalada.

As diferenças observadas mostram apenas os valores registrados na base e
não permitem afirmar as causas dessas diferenças.
""")


# ==========================================
# POTÊNCIA AO LONGO DO TEMPO
# ==========================================

if "AnoReferencia" in df.columns and "MesReferencia" in df.columns:

    potencia_tempo = (
        df.groupby(
            ["AnoReferencia", "MesReferencia"]
        )[coluna_potencia]
        .sum()
        .reset_index()
    )

    potencia_tempo["Data"] = pd.to_datetime(
        potencia_tempo["AnoReferencia"].astype(str)
        + "-"
        + potencia_tempo["MesReferencia"].astype(str)
        + "-01",
        errors="coerce"
    )

    potencia_tempo = potencia_tempo.sort_values("Data")

    st.subheader(
        "Houve mudanças na potência ao longo do tempo?"
    )

    fig_tempo = px.line(
        potencia_tempo,
        x="Data",
        y=coluna_potencia,
        title="Potência instalada ao longo do tempo",
        markers=True
    )

    st.plotly_chart(
        fig_tempo,
        use_container_width=True
    )

    st.markdown("""
    ### O que podemos observar?

    O gráfico mostra como a potência instalada registrada varia ao longo do tempo.

    É possível identificar períodos em que os valores aumentaram ou diminuíram.

    A base mostra essas variações, mas não permite afirmar quais foram as causas
    dessas mudanças.
    """)


# ==========================================
# INFORMAÇÕES IMPORTANTES
# ==========================================

st.markdown("""
### Informações importantes

- A potência instalada é medida em kW.
- Os dados permitem comparar os estados.
- O gráfico de barras mostra as diferenças entre os estados.
- O gráfico de linha mostra a variação ao longo do tempo.
- Os dados não permitem determinar as causas das variações observadas.
""")
