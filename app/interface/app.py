import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.dados import alunos
from src.estatisticas import media, mediana, minimo, maximo, contagem
from src.transformacoes import identificar_categoria
# ==========================================
# CONFIGURAÇÃO DA INTERFACE
# ==========================================

st.set_page_config(
    page_title="Análise Escolar",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# DADOS
# ==========================================

notas_g1 = tuple(map(lambda aluno: aluno["G1"], alunos))
notas_g2 = tuple(map(lambda aluno: aluno["G2"], alunos))
notas_g3 = tuple(map(lambda aluno: aluno["G3"], alunos))


# ==========================================
# DADOS: PROFISSÃO DOS PAIS
# ==========================================

dados_profissoes = tuple(
    map(
        lambda aluno: {
            "Profissão da mãe": identificar_categoria(aluno, "Mjob_"),
            "Profissão do pai": identificar_categoria(aluno, "Fjob_"),
            "Nota final": aluno["G3"]
        },
        alunos
    )
)

df_profissoes = pd.DataFrame(dados_profissoes)

# ==========================================
# MENU LATERAL
# ==========================================

st.sidebar.title("📊 Análise Escolar")
st.sidebar.caption("Sistema de análise de desempenho")

pagina = st.sidebar.selectbox(
    "Navegação",
    [
        "Visão geral",
        "G1 - Primeira avaliação",
        "G2 - Segunda avaliação",
        "G3 - Avaliação final",
        "Profissão dos pais"
    ]
)


# ==========================================
# VISÃO GERAL
# ==========================================

if pagina == "Visão geral":

    st.title("Visão geral")
    st.write("Indicadores gerais do desempenho escolar.")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total de alunos", len(alunos))
    col2.metric("Média G1", f"{media(notas_g1):.2f}")
    col3.metric("Média G2", f"{media(notas_g2):.2f}")
    col4.metric("Média G3", f"{media(notas_g3):.2f}")

    st.divider()

    st.subheader("Comparação entre avaliações")

    medias = {
        "Avaliação": ["G1", "G2", "G3"],
        "Média": [
            media(notas_g1),
            media(notas_g2),
            media(notas_g3)
        ]
    }

    grafico = px.bar(
        medias,
        x="Avaliação",
        y="Média",
        text_auto=".2f",
        title="Média das notas por avaliação",
        color="Avaliação"
    )

    grafico.update_layout(
        yaxis_title="Nota média",
        xaxis_title="Avaliação",
        showlegend=False
    )

    st.plotly_chart(grafico, use_container_width=True)

    st.subheader("Distribuição das notas")

    distribuicao = px.histogram(
        x=notas_g3,
        nbins=21,
        title="Distribuição das notas finais (G3)",
        labels={"x": "Nota", "y": "Quantidade de alunos"}
    )

    st.plotly_chart(distribuicao, use_container_width=True)


# ==========================================
# PÁGINAS DE AVALIAÇÃO
# ==========================================

elif pagina in [
    "G1 - Primeira avaliação",
    "G2 - Segunda avaliação",
    "G3 - Avaliação final"
]:

    avaliacao = {
        "G1 - Primeira avaliação": ("G1", notas_g1),
        "G2 - Segunda avaliação": ("G2", notas_g2),
        "G3 - Avaliação final": ("G3", notas_g3)
    }

    nome, notas = avaliacao[pagina]

    st.title(f"Análise de {nome}")
    st.write(f"Estatísticas referentes à avaliação {nome}.")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Média", f"{media(notas):.2f}")
    col2.metric("Mediana", f"{mediana(notas):.2f}")
    col3.metric("Menor nota", minimo(notas))
    col4.metric("Maior nota", maximo(notas))

    st.divider()

    st.subheader("Distribuição das notas")

    grafico = px.histogram(
        x=notas,
        nbins=21,
        title=f"Distribuição de notas - {nome}",
        labels={"x": "Nota", "y": "Quantidade de alunos"}
    )

    st.plotly_chart(grafico, use_container_width=True)

    st.subheader("Indicadores de desempenho")

    quantidade_acima_10 = contagem(
        notas,
        lambda nota: nota >= 10
    )

    quantidade_abaixo_10 = contagem(
        notas,
        lambda nota: nota < 10
    )

    col1, col2 = st.columns(2)

    col1.metric("Notas a partir de 10", quantidade_acima_10)
    col2.metric("Notas abaixo de 10", quantidade_abaixo_10)

    st.caption(
        "A divisão entre notas a partir de 10 e abaixo de 10 "
        "é apenas um critério de análise da avaliação parcial."
    )

# ==========================================
# PROFISSÃO DOS PAIS
# ==========================================

elif pagina == "Profissão dos pais":

    st.title("Profissão dos pais e desempenho escolar")

    st.write(
        "Análise da distribuição das notas finais (G3) "
        "de acordo com a profissão dos pais."
    )

    st.divider()

    # ------------------------------------------
    # PROFISSÃO DA MÃE
    # ------------------------------------------

    st.subheader("Profissão da mãe")

    grafico_mae = px.box(
        df_profissoes,
        x="Profissão da mãe",
        y="Nota final",
        color="Profissão da mãe",
        points="all",
        title="Distribuição das notas por profissão da mãe"
    )

    grafico_mae.update_layout(
        xaxis_title="Profissão da mãe",
        yaxis_title="Nota final (G3)",
        showlegend=False
    )

    st.plotly_chart(grafico_mae, use_container_width=True)

    st.divider()

    # ------------------------------------------
    # PROFISSÃO DO PAI
    # ------------------------------------------

    st.subheader("Profissão do pai")

    grafico_pai = px.box(
        df_profissoes,
        x="Profissão do pai",
        y="Nota final",
        color="Profissão do pai",
        points="all",
        title="Distribuição das notas por profissão do pai"
    )

    grafico_pai.update_layout(
        xaxis_title="Profissão do pai",
        yaxis_title="Nota final (G3)",
        showlegend=False
    )

    st.plotly_chart(grafico_pai, use_container_width=True)

    st.caption(
        "O Box Plot permite comparar medianas, dispersões e "
        "valores atípicos. As diferenças observadas não "
        "comprovam uma relação de causa e efeito."
    )