import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.dados import carregar_disciplina
from src.estatisticas import media, mediana, minimo, maximo, contagem
from src.transformacoes import identificar_categoria, remover_nota_zero
from src.validações import verificar_limites, verificar_binarias
from src.analises import (
    resumo_geral,
    analise_por_grupo,
    analise_por_faltas,
    NOMES_FAIXAS,
)
from src.organização import (
    CAMINHOS_CSV,
    CODIFICACAO_BINARIA,
    VARIAVEIS_NUMERICAS,
    VARIAVEIS_ORDINAIS,
)
from src.correlacao import (
    valores,
    matriz_correlacao,
    matriz_em_linhas,
    coeficiente,
    inclinacao,
    intercepto,
    r_quadrado,
    forca_associacao,
    direcao_associacao,
    registros_por_grupo,
    resumo_por_grupo,
)

# ==========================================
# CONFIGURAÇÃO DA INTERFACE
# ==========================================

st.set_page_config(
    page_title="Análise Escolar",
    page_icon="📊",
    layout="wide"
)

# Variáveis oferecidas na análise de correlação
VARIAVEIS_CORRELACAO = (
    VARIAVEIS_NUMERICAS
    + VARIAVEIS_ORDINAIS
    + tuple(CODIFICACAO_BINARIA)
)

# Seleção inicial da matriz (numéricas e ordinais, sem as binárias)
VARIAVEIS_PADRAO = VARIAVEIS_NUMERICAS + VARIAVEIS_ORDINAIS

# Variáveis que podem ser usadas para agrupar alunos
VARIAVEIS_CATEGORICAS = tuple(CODIFICACAO_BINARIA) + (
    "studytime", "failures", "Medu", "Fedu", "traveltime",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health",
)


# ==========================================
# MENU LATERAL E FILTROS GLOBAIS
# ==========================================

st.sidebar.title("📊 Análise Escolar")
st.sidebar.caption("Sistema de análise de desempenho")

disciplina = st.sidebar.selectbox(
    "Disciplina (arquivo)",
    list(CAMINHOS_CSV)
)

excluir_zeros = st.sidebar.checkbox(
    "Excluir alunos com G3 = 0",
    value=True,
    help=(
        "Decisão adotada: G3 = 0 indica, na maioria dos casos, "
        "abandono ou não conclusão, e não nota baixa. "
        "Veja a seção 'Decisões de análise' do README."
    )
)

pagina = st.sidebar.selectbox(
    "Navegação",
    [
        "Visão geral",
        "G1 - Primeira avaliação",
        "G2 - Segunda avaliação",
        "G3 - Avaliação final",
        "Análises da proposta",
        "Profissão dos pais",
        "Análise de correlação",
    ]
)


# ==========================================
# CARREGAMENTO COM TRATAMENTO DE ERRO
# ==========================================

try:
    alunos_brutos = carregar_disciplina(disciplina)
except FileNotFoundError:
    st.error(
        f"Arquivo de {disciplina} não encontrado: "
        f"{CAMINHOS_CSV[disciplina]}. Verifique se a pasta dados/ "
        "contém o CSV."
    )
    st.stop()
except (ValueError, KeyError) as erro:
    st.error(
        f"O arquivo de {disciplina} tem um valor ou coluna inesperada "
        f"({erro}). Confira o formato: separador ';' e colunas do "
        "dicionário de dados."
    )
    st.stop()

if len(alunos_brutos) == 0:
    st.error(f"O arquivo de {disciplina} não tem nenhum registro.")
    st.stop()


# ==========================================
# VALIDAÇÃO DOS DADOS
# ==========================================

# Pares (coluna, registros fora da regra) que não estão vazios
problemas_validacao = tuple(
    filter(
        lambda par: len(par[1]) > 0,
        verificar_limites(alunos_brutos) + verificar_binarias(alunos_brutos)
    )
)

with st.sidebar.expander("Validação dos dados"):
    if problemas_validacao:
        st.warning(
            "Colunas com valores fora da regra: "
            + ", ".join(
                f"{coluna} ({len(registros)})"
                for coluna, registros in problemas_validacao
            )
        )
    else:
        st.success(
            f"Nenhum valor fora da regra em {len(alunos_brutos)} registros."
        )


# ==========================================
# DADOS
# ==========================================

alunos = remover_nota_zero(alunos_brutos) if excluir_zeros else alunos_brutos

notas_g1 = tuple(map(lambda aluno: aluno["G1"], alunos))
notas_g2 = tuple(map(lambda aluno: aluno["G2"], alunos))
notas_g3 = tuple(map(lambda aluno: aluno["G3"], alunos))

st.sidebar.caption(
    f"Alunos considerados: {len(alunos)} de {len(alunos_brutos)}"
)


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
# VISÃO GERAL
# ==========================================

if pagina == "Visão geral":

    st.title(f"Visão geral — {disciplina}")
    st.write("Indicadores gerais do desempenho escolar.")

    if len(alunos) == 0:
        st.warning("Nenhum aluno restou após os filtros.")
        st.stop()

    resumo = resumo_geral(alunos)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total de alunos", resumo["total"])
    col2.metric(
        "Aprovados (G3 ≥ 10)",
        resumo["aprovados"],
        f"{resumo['percentual_aprovados'] * 100:.1f}%"
    )
    col3.metric(
        "Reprovados (G3 < 10)",
        resumo["reprovados"],
        f"{resumo['percentual_reprovados'] * 100:.1f}%",
        delta_color="off"
    )
    col4.metric("Média G3", f"{resumo['media']:.2f}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Média G1", f"{media(notas_g1):.2f}")
    col2.metric("Média G2", f"{media(notas_g2):.2f}")
    col3.metric("Mediana G3", f"{resumo['mediana']:.2f}")
    col4.metric(
        "Amplitude de G3",
        f"{resumo['minimo']} a {resumo['maximo']}"
    )

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

    st.title(f"Análise de {nome} — {disciplina}")
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
# ANÁLISES DA PROPOSTA (§6.3, §6.4, §6.5)
# ==========================================

elif pagina == "Análises da proposta":

    st.title(f"Análises da proposta — {disciplina}")
    st.write(
        "Desempenho por tempo de estudo, faltas e reprovações anteriores. "
        "Aprovação segue a regra G3 ≥ 10. Diferenças são descritivas, "
        "não comprovam causa e efeito."
    )

    # (título, coluna, ordem das categorias, explicação)
    grupos_proposta = (
        (
            "Tempo de estudo (studytime)",
            "studytime",
            ("1", "2", "3", "4"),
            "Tempo semanal: 1 (<2h), 2 (2–5h), 3 (5–10h), 4 (>10h).",
        ),
        (
            "Faltas por faixa",
            "faixa_faltas",
            NOMES_FAIXAS,
            "Faixas definidas em organização.py (FAIXAS_FALTAS).",
        ),
        (
            "Reprovações anteriores (failures)",
            "failures",
            ("0", "1", "2", "3"),
            "Número de reprovações anteriores, não o resultado atual.",
        ),
    )

    # Linhas (rótulo, quantidade, média de G3, proporção de aprovados)
    linhas_grupo = lambda grupo: (
        analise_por_faltas(alunos)
        if grupo[1] == "faixa_faltas"
        else analise_por_grupo(alunos, grupo[1], grupo[2])
    )

    # Tabela com percentual em escala de 0 a 100
    tabela_grupo = lambda grupo: pd.DataFrame(
        tuple(
            map(
                lambda linha: (
                    linha[0], linha[1],
                    round(linha[2], 2), round(linha[3] * 100, 1)
                ),
                linhas_grupo(grupo)
            )
        ),
        columns=[grupo[0], "Alunos", "Média de G3", "% aprovados"]
    )

    # Renderiza título, tabela e gráfico de um grupo
    renderizar_grupo = lambda grupo: (
        st.subheader(grupo[0]),
        st.caption(grupo[3]),
        st.dataframe(tabela_grupo(grupo), hide_index=True, use_container_width=True),
        st.plotly_chart(
            px.bar(
                tabela_grupo(grupo),
                x=grupo[0],
                y="% aprovados",
                text_auto=".1f",
                title=f"Percentual de aprovados por {grupo[0].lower()}"
            ),
            use_container_width=True
        ),
        st.divider(),
    )

    tuple(map(renderizar_grupo, grupos_proposta))


# ==========================================
# PROFISSÃO DOS PAIS
# ==========================================

elif pagina == "Profissão dos pais":

    st.title(f"Profissão dos pais e desempenho escolar — {disciplina}")

    st.write(
        "Análise da distribuição das notas finais (G3) "
        "de acordo com a profissão dos pais."
    )

    st.divider()

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


# ==========================================
# ANÁLISE DE CORRELAÇÃO
# ==========================================

elif pagina == "Análise de correlação":

    st.title(f"Análise de correlação — {disciplina}")
    st.write(
        "Associações entre variáveis do conjunto de dados. "
        "Correlação indica associação, não causalidade."
    )

    metodo = st.radio(
        "Método de correlação",
        ("Pearson", "Spearman"),
        horizontal=True,
        help=(
            "Pearson mede relação linear. "
            "Spearman mede relação monotônica e é mais adequado "
            "para variáveis ordinais."
        )
    )

    # ------------------------------------------
    # 1. MATRIZ DE CORRELAÇÃO
    # ------------------------------------------

    st.subheader("1. Matriz de correlação")

    variaveis_matriz = st.multiselect(
        "Variáveis da matriz",
        VARIAVEIS_CORRELACAO,
        default=VARIAVEIS_PADRAO
    )

    if len(variaveis_matriz) >= 2:

        matriz = matriz_correlacao(alunos, variaveis_matriz, metodo)

        mapa_calor = px.imshow(
            matriz_em_linhas(matriz, variaveis_matriz),
            x=variaveis_matriz,
            y=variaveis_matriz,
            zmin=-1,
            zmax=1,
            color_continuous_scale="RdBu_r",
            text_auto=".2f",
            aspect="auto",
            title=f"Matriz de correlação ({metodo})"
        )

        st.plotly_chart(mapa_calor, use_container_width=True)

    else:
        st.info("Selecione pelo menos duas variáveis para montar a matriz.")

    st.divider()

    # ------------------------------------------
    # 2. ANÁLISE INDIVIDUAL
    # ------------------------------------------

    st.subheader("2. Análise individual")

    col_x, col_y = st.columns(2)

    variavel_x = col_x.selectbox(
        "Variável X",
        VARIAVEIS_CORRELACAO,
        index=VARIAVEIS_CORRELACAO.index("studytime")
    )

    variavel_y = col_y.selectbox(
        "Variável Y",
        VARIAVEIS_CORRELACAO,
        index=VARIAVEIS_CORRELACAO.index("G3")
    )

    x = valores(alunos, variavel_x)
    y = valores(alunos, variavel_y)

    r = coeficiente(x, y, metodo)
    r2 = r_quadrado(x, y)
    b = inclinacao(x, y)
    a = intercepto(x, y)

    dispersao = px.scatter(
        x=x,
        y=y,
        opacity=0.5,
        labels={"x": variavel_x, "y": variavel_y},
        title=f"{variavel_x} × {variavel_y}"
    )

    if a is not None:
        extremos = (min(x), max(x))
        dispersao.add_scatter(
            x=extremos,
            y=(a + b * extremos[0], a + b * extremos[1]),
            mode="lines",
            name="Linha de tendência (regressão linear)"
        )

    st.plotly_chart(dispersao, use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(f"Coeficiente {metodo}", "—" if r is None else f"{r:.2f}")
    col2.metric("Força", forca_associacao(r))
    col3.metric("Direção", direcao_associacao(r))
    col4.metric("r²", "—" if r2 is None else f"{r2:.2f}")

    st.caption(
        "A linha de tendência é a regressão linear simples, mesmo "
        "quando o coeficiente exibido é Spearman. "
        f"Pares analisados: {len(alunos)}."
    )

    st.divider()

    # ------------------------------------------
    # 3. COMPARAÇÃO POR CATEGORIAS
    # ------------------------------------------

    st.subheader("3. Comparação por categorias")

    categoria = st.selectbox(
        "Variável de agrupamento",
        VARIAVEIS_CATEGORICAS
    )

    caixas = px.box(
        pd.DataFrame(registros_por_grupo(alunos, categoria)),
        x="Grupo",
        y="G3",
        color="Grupo",
        points="all",
        title=f"Nota final (G3) por {categoria}"
    )

    caixas.update_layout(
        xaxis_title=categoria,
        yaxis_title="Nota final (G3)",
        showlegend=False
    )

    st.plotly_chart(caixas, use_container_width=True)

    tabela_grupos = pd.DataFrame(
        resumo_por_grupo(alunos, categoria),
        columns=[categoria, "Alunos", "Média de G3"]
    )

    st.dataframe(
        tabela_grupos.round({"Média de G3": 2}),
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "Diferenças entre grupos são descritivas. Não comprovam "
        "relação de causa e efeito, e grupos pequenos têm médias instáveis."
    )
