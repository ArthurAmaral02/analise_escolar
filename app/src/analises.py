# ==========================================
# MÓDULO DE ANÁLISES DA PROPOSTA (funções puras)
# ==========================================


from src.estatisticas import media, mediana, minimo, maximo, contagem, proporcao
from src.transformacoes import agrupar_por, adicionar_faixa_faltas
from src.correlacao import valores, rotulo
from src.organização import NOTA_MINIMA_APROVACAO, FAIXAS_FALTAS


# Nomes das faixas de faltas, na ordem definida em organização.py
NOMES_FAIXAS = tuple(
    map(lambda faixa: faixa[0], FAIXAS_FALTAS)
)

# Regra analítica de aprovação (G3 >= 10)
aprovado = lambda aluno: aluno["G3"] >= NOTA_MINIMA_APROVACAO


# ==========================================
# 6.1 RESUMO GERAL
# ==========================================

# Totais, percentuais e estatísticas de G3 para um conjunto de alunos
resumo_geral = lambda alunos: {
    "total": len(alunos),
    "aprovados": contagem(alunos, aprovado),
    "reprovados": contagem(alunos, lambda aluno: not aprovado(aluno)),
    "percentual_aprovados": proporcao(alunos, aprovado),
    "percentual_reprovados": proporcao(
        alunos, lambda aluno: not aprovado(aluno)
    ),
    "media": media(valores(alunos, "G3")),
    "mediana": mediana(valores(alunos, "G3")),
    "minimo": minimo(valores(alunos, "G3")),
    "maximo": maximo(valores(alunos, "G3")),
}


# ==========================================
# 6.3, 6.4 e 6.5 ANÁLISES POR GRUPO
# ==========================================

# Ordena linhas (rótulo, ...) pela ordem dada; rótulos fora da ordem vão ao fim
ordenar_por = lambda linhas, ordem: tuple(
    sorted(
        linhas,
        key=lambda linha: (
            ordem.index(linha[0]) if linha[0] in ordem else len(ordem)
        )
    )
)

# Para cada grupo: (rótulo, quantidade, média de G3, % de aprovados)
analise_por_grupo = lambda alunos, coluna, ordem=(): ordenar_por(
    tuple(
        map(
            lambda item: (
                rotulo(coluna, item[0]),
                len(item[1]),
                media(valores(item[1], "G3")),
                proporcao(item[1], aprovado)
            ),
            agrupar_por(alunos, coluna).items()
        )
    ),
    ordem
)

# Adiciona a faixa de faltas a cada aluno (sem alterar o original)
alunos_com_faixa = lambda alunos: tuple(
    map(adicionar_faixa_faltas, alunos)
)

# Análise por faixas de faltas, na ordem das faixas
analise_por_faltas = lambda alunos: analise_por_grupo(
    alunos_com_faixa(alunos),
    "faixa_faltas",
    NOMES_FAIXAS
)
