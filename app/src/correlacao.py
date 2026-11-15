# ==========================================
# MÓDULO DE CORRELAÇÃO (funções puras)
# ==========================================
# Pearson e Spearman implementados com a biblioteca padrão.
# Nenhuma função imprime, lê arquivos ou altera os registros recebidos.

import math

from src.estatisticas import media, contagem
from src.transformacoes import agrupar_por
from src.organização import CODIFICACAO_BINARIA


# ==========================================
# EXTRAÇÃO DE VALORES
# ==========================================

# Valores de uma coluna, na ordem dos alunos
valores = lambda alunos, coluna: tuple(
    map(lambda aluno: aluno[coluna], alunos)
)

# Rótulos legíveis para colunas binárias (ex.: 0 -> "GP")
ROTULOS_BINARIOS = {
    coluna: {codigo: texto for texto, codigo in mapa.items()}
    for coluna, mapa in CODIFICACAO_BINARIA.items()
}

# Converte o código de uma coluna no rótulo exibido
rotulo = lambda coluna, valor: ROTULOS_BINARIOS.get(coluna, {}).get(
    valor, str(valor)
)


# ==========================================
# DESVIOS E SOMAS
# ==========================================

# Desvios em relação à média
desvios = lambda vetor: (
    lambda m: tuple(v - m for v in vetor)
)(media(vetor))

# Soma dos quadrados dos desvios
soma_quadrados = lambda vetor: sum(d * d for d in desvios(vetor))

# Soma dos produtos dos desvios (base da covariância)
soma_produtos = lambda x, y: sum(
    a * b for a, b in zip(desvios(x), desvios(y))
)


# ==========================================
# CORRELAÇÃO
# ==========================================

# Correlação de Pearson (relação linear).
# Retorna None quando não há variação suficiente.
pearson = lambda x, y: (
    soma_produtos(x, y) / math.sqrt(soma_quadrados(x) * soma_quadrados(y))
    if len(x) == len(y) > 1
    and soma_quadrados(x) > 0
    and soma_quadrados(y) > 0
    else None
)

# Postos com empates resolvidos pela média dos postos
postos = lambda vetor: tuple(
    contagem(vetor, lambda w: w < v)
    + (contagem(vetor, lambda w: w == v) + 1) / 2
    for v in vetor
)

# Correlação de Spearman (relação monotônica): Pearson sobre os postos
spearman = lambda x, y: pearson(postos(x), postos(y))

# Escolhe o método pelo nome exibido na interface
coeficiente = lambda x, y, metodo: (
    spearman(x, y) if metodo == "Spearman" else pearson(x, y)
)

# Matriz de correlação como dicionário {(variável_a, variável_b): r}
matriz_correlacao = lambda alunos, variaveis, metodo: {
    (a, b): coeficiente(
        valores(alunos, a), valores(alunos, b), metodo
    )
    for a in variaveis
    for b in variaveis
}

# Matriz como lista de linhas para o gráfico (None vira NaN)
matriz_em_linhas = lambda matriz, variaveis: [
    [
        math.nan if matriz[(a, b)] is None else matriz[(a, b)]
        for b in variaveis
    ]
    for a in variaveis
]


# ==========================================
# REGRESSÃO LINEAR SIMPLES (para a linha de tendência)
# ==========================================

# Inclinação da reta y = a + b * x
inclinacao = lambda x, y: (
    soma_produtos(x, y) / soma_quadrados(x)
    if soma_quadrados(x) > 0
    else None
)

# Intercepto da reta y = a + b * x
intercepto = lambda x, y: (
    media(y) - inclinacao(x, y) * media(x)
    if inclinacao(x, y) is not None
    else None
)

# Coeficiente de determinação (r²)
r_quadrado = lambda x, y: (
    None if pearson(x, y) is None else pearson(x, y) ** 2
)


# ==========================================
# INTERPRETAÇÃO DESCRITIVA
# ==========================================

# Força da associação, em palavras (critério descritivo, não inferencial)
forca_associacao = lambda r: (
    "sem dados suficientes" if r is None
    else "desprezível" if abs(r) < 0.1
    else "fraca" if abs(r) < 0.3
    else "moderada" if abs(r) < 0.5
    else "forte"
)

# Direção da associação
direcao_associacao = lambda r: (
    "não se aplica" if r is None
    else "positiva" if r > 0
    else "negativa" if r < 0
    else "nula"
)


# ==========================================
# COMPARAÇÃO POR CATEGORIAS
# ==========================================

# Registros prontos para o gráfico de caixa: {"Grupo": rótulo, "G3": nota}
registros_por_grupo = lambda alunos, coluna: tuple(
    map(
        lambda aluno: {
            "Grupo": rotulo(coluna, aluno[coluna]),
            "G3": aluno["G3"]
        },
        alunos
    )
)

# Resumo por grupo: (rótulo, quantidade de alunos, média de G3)
resumo_por_grupo = lambda alunos, coluna: tuple(
    (
        rotulo(coluna, valor),
        len(grupo),
        media(valores(grupo, "G3"))
    )
    for valor, grupo in agrupar_por(alunos, coluna).items()
)
