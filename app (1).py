import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Dashboard de Dados",
    layout="wide"
)

st.title("Dashboard de Dados")

df = pd.read_csv("capacidade-instalada-geracao-uf.csv", encoding="latin-1")

if arquivo is not None:

    df = pd.read_csv(arquivo)

    # Remover espaços dos nomes das colunas
    df.columns = df.columns.str.strip()

    # Corrigir a coluna de potência
    df["MdaPotenciaInstaladakW"] = pd.to_numeric(
        df["MdaPotenciaInstaladakW"]
        .astype(str)
        .str.replace(",", "."),
        errors="coerce"
    )

    # Visualização dos dados
    st.subheader("Visualização dos dados")
    st.dataframe(df.head())

    # Quantidade de registros e colunas
    col1, col2 = st.columns(2)

    col1.metric(
        "Quantidade de registros",
        df.shape[0]
    )

    col2.metric(
        "Quantidade de colunas",
        df.shape[1]
    )

    # Verificação dos dados
    st.subheader("Verificação dos dados")

    st.write("Valores ausentes:")
    st.write(df.isnull().sum())

    st.write("Quantidade de linhas duplicadas:")
    st.write(df.duplicated().sum())

    st.write("Tipos de dados:")
    st.write(df.dtypes)

    # Maior potência
    maior = df.loc[
        df["MdaPotenciaInstaladakW"].idxmax()
    ]

    st.subheader("Estado com maior potência instalada")

    st.write(
        maior["NomUF"],
        maior["MdaPotenciaInstaladakW"],
        "kW"
    )

    # Menor potência
    menor = df.loc[
        df["MdaPotenciaInstaladakW"].idxmin()
    ]

    st.subheader("Estado com menor potência instalada")

    st.write(
        menor["NomUF"],
        menor["MdaPotenciaInstaladakW"],
        "kW"
    )

    # Gráfico de potência por estado
    fig = px.bar(
        df,
        x="NomUF",
        y="MdaPotenciaInstaladakW",
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

    # Potência ao longo do tempo
    potencia_tempo = (
        df.groupby(
            ["AnoReferencia", "MesReferencia"]
        )["MdaPotenciaInstaladakW"]
        .sum()
        .reset_index()
    )

    potencia_tempo["Data"] = pd.to_datetime(
        potencia_tempo["AnoReferencia"].astype(str)
        + "-"
        + potencia_tempo["MesReferencia"].astype(str)
        + "-01"
    )

    potencia_tempo = potencia_tempo.sort_values("Data")

    st.subheader(
        "Houve mudanças na potência ao longo do tempo?"
    )

    fig_tempo = px.line(
        potencia_tempo,
        x="Data",
        y="MdaPotenciaInstaladakW",
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

    st.markdown("""
    ### Informações importantes

    - A potência instalada é medida em kW.
    - Os dados permitem comparar os estados.
    - O gráfico de barras mostra as diferenças entre os estados.
    - O gráfico de linha mostra a variação ao longo do tempo.
    - Os dados não permitem determinar as causas das variações observadas..
    """)