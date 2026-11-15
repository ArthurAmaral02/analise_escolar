
# ==========================================
# MÓDULO DE TRANSFORMAÇÕES DOS ALUNOS
# ==========================================
from src.organização import NOTA_MINIMA_APROVACAO, FAIXAS_FALTAS
from src.estatisticas import somar

# ==========================================
# VALIDAÇÃO
# ==========================================

# Verifica se G3 é um inteiro entre 0 e 20
nota_valida = lambda aluno: (
    type(aluno.get("G3")) is int
    and 0 <= aluno["G3"] <= 20
)

# Filtra alunos com notas válidas
notas_validas = lambda alunos: tuple(
    filter(nota_valida, alunos)
)


# ==========================================
# CLASSIFICAÇÃO
# ==========================================

# Classifica o resultado do aluno
classificar_resultado = lambda nota: (
    "Aprovado"
    if nota >= NOTA_MINIMA_APROVACAO
    else "Reprovado"
)

# Identifica a faixa de faltas (primeira faixa que contém o valor)
faixa_faltas = lambda faltas: next(
    map(
        lambda faixa: faixa[0],
        filter(
            lambda faixa: faltas >= faixa[1]
            and (faixa[2] is None or faltas <= faixa[2]),
            FAIXAS_FALTAS
        )
    ),
    None
)


# ==========================================
# TRANSFORMAÇÃO DE REGISTROS
# ==========================================

# Adiciona o resultado ao registro do aluno
adicionar_resultado = lambda aluno: {
    **aluno,
    "resultado": classificar_resultado(aluno["G3"])
}

# Adiciona a faixa de faltas ao registro
adicionar_faixa_faltas = lambda aluno: {
    **aluno,
    "faixa_faltas": faixa_faltas(aluno["absences"])
}


# ==========================================
# AGRUPAMENTO
# ==========================================

# Agrupa registros de acordo com uma coluna
agrupar_por = lambda registros, coluna: dict(
    map(
        lambda valor: (
            valor,
            tuple(
                filter(
                    lambda registro: registro[coluna] == valor,
                    registros
                )
            )
        ),
        sorted(set(map(lambda registro: registro[coluna], registros)))
    )
)

# Remove alunos sem nota final (G3 = 0), sem alterar a tupla original
remover_nota_zero = lambda alunos: tuple(
    filter(lambda aluno: aluno["G3"] != 0, alunos)
)


# ==========================================
# PREPARAÇÃO DOS ALUNOS
# ==========================================

# Valida, classifica e acrescenta a faixa de faltas
preparar_alunos = lambda alunos: tuple(
    map(
        lambda aluno: {
            **adicionar_resultado(aluno),
            "faixa_faltas": faixa_faltas(aluno["absences"])
        },
        notas_validas(alunos)
    )
)



# ==========================================
# COMPARAÇÃO: PROFISSÃO DOS PAIS E NOTAS
# ==========================================

# Identifica a profissão a partir das colunas One-Hot
identificar_categoria = lambda aluno, prefixo: next(
    map(
        lambda par: par[0].replace(prefixo, ""),
        filter(
            lambda par: par[0].startswith(prefixo) and par[1] == 1,
            aluno.items()
        )
    ),
    "desconhecido"
)

# Calcula a média de G3 de um grupo de alunos
media_notas = lambda alunos: (
    somar(map(lambda aluno: aluno["G3"], alunos)) / len(alunos)
    if alunos else 0
)

# Média de G3 por profissão, para um prefixo one-hot ("Mjob_" ou "Fjob_")
media_por_profissao = lambda alunos, prefixo: dict(
    map(
        lambda profissao: (
            profissao,
            media_notas(
                tuple(
                    filter(
                        lambda aluno: identificar_categoria(aluno, prefixo) == profissao,
                        alunos
                    )
                )
            )
        ),
        sorted(set(map(lambda aluno: identificar_categoria(aluno, prefixo), alunos)))
    )
)

# Agrupa os alunos pela profissão da mãe e calcula as médias
media_por_profissao_mae = lambda alunos: media_por_profissao(alunos, "Mjob_")

# Agrupa os alunos pela profissão do pai e calcula as médias
media_por_profissao_pai = lambda alunos: media_por_profissao(alunos, "Fjob_")
