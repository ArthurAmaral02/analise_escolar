from src.organização import LIMITES_VARIAVEIS, COLUNAS_BINARIAS, GRUPOS_ONE_HOT, TODAS_VARIAVEIS,VARIAVEIS_ORIGINAIS

verificar_ausentes = lambda alunos: tuple(
    map(
        lambda coluna: (
            coluna,
            sum(
                map(
                    lambda aluno: aluno[coluna] is None,
                    alunos
                )
            )
        ),
        alunos[0].keys()
    )
)


verificar_limites = lambda alunos: tuple(
    map(
        lambda coluna: (
            coluna,
            tuple(
                filter(
                    lambda aluno: not (
                        LIMITES_VARIAVEIS[coluna][0]
                        <= aluno[coluna]
                        <= LIMITES_VARIAVEIS[coluna][1]
                    ),
                    alunos
                )
            )
        ),
        LIMITES_VARIAVEIS.keys()
    )
)


verificar_binarias = lambda alunos: tuple(
    map(
        lambda coluna: (
            coluna,
            tuple(
                filter(
                    lambda aluno: aluno[coluna] not in (0, 1),
                    alunos
                )
            )
        ),
        COLUNAS_BINARIAS
    )
)

verificar_one_hot = lambda alunos: tuple(
    map(
        lambda grupo: (
            grupo,
            tuple(
                filter(
                    lambda aluno: sum(
                        map(lambda coluna: aluno[coluna], GRUPOS_ONE_HOT[grupo])
                    ) != 1,
                    alunos
                )
            )
        ),
        GRUPOS_ONE_HOT.keys()
    )
)

import math

verificar_nan = lambda alunos: tuple(
    map(
        lambda coluna: (
            coluna,
            sum(
                map(
                    lambda aluno: (
                        isinstance(aluno[coluna], float)
                        and math.isnan(aluno[coluna])
                    ),
                    alunos
                )
            )
        ),
        alunos[0].keys()
    )
)

verificar_classificacao = lambda: {
    "total_classificadas": len(TODAS_VARIAVEIS),
    "total_distintas": len(set(TODAS_VARIAVEIS)),
    "variaveis_nao_classificadas": tuple(
        filter(
            lambda coluna: coluna not in TODAS_VARIAVEIS,
            VARIAVEIS_ORIGINAIS
        )
    ),
    "variaveis_extras": tuple(
        filter(
            lambda coluna: coluna not in VARIAVEIS_ORIGINAIS,
            TODAS_VARIAVEIS
        )
    )
}
