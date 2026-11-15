
# ==========================================
# MÓDULO DE TRANSFORMAÇÕES DOS ALUNOS
# ==========================================
from src.organização import NOTA_MINIMA_APROVACAO, FAIXAS_FALTAS

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

# Identifica a faixa de faltas
faixa_faltas = lambda faltas: next(
    (
        nome
        for nome, minimo, maximo in FAIXAS_FALTAS
        if faltas >= minimo
        and (maximo is None or faltas <= maximo)
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
        sorted({registro[coluna] for registro in registros})
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
    (
        coluna.replace(prefixo, "")
        for coluna, valor in aluno.items()
        if coluna.startswith(prefixo) and valor == 1
    ),
    "desconhecido"
)

# Calcula a média de G3 de um grupo de alunos
media_notas = lambda alunos: (
    sum(map(lambda aluno: aluno["G3"], alunos)) / len(alunos)
    if alunos else 0
)

# Agrupa os alunos pela profissão da mãe e calcula as médias
media_por_profissao_mae = lambda alunos: {
    profissao: media_notas(
        tuple(
            filter(
                lambda aluno: identificar_categoria(aluno, "Mjob_") == profissao,
                alunos
            )
        )
    )
    for profissao in sorted({
        identificar_categoria(aluno, "Mjob_")
        for aluno in alunos
    })
}

# Agrupa os alunos pela profissão do pai e calcula as médias
media_por_profissao_pai = lambda alunos: {
    profissao: media_notas(
        tuple(
            filter(
                lambda aluno: identificar_categoria(aluno, "Fjob_") == profissao,
                alunos
            )
        )
    )
    for profissao in sorted({
        identificar_categoria(aluno, "Fjob_")
        for aluno in alunos
    })
}
