import csv
from pathlib import Path

from src.organização import DELIMITADOR, CAMINHOS_CSV, COLUNAS_INTEIRAS, CODIFICACAO_BINARIA, CATEGORIAS_NOMINAIS


# ==========================================
# LEITURA (sem efeitos colaterais no import)
# ==========================================

# Converte uma linha do CSV em registro de aluno (inteiros, binárias e one-hot)
transformar_linha = lambda linha: {
    **dict(
        map(
            lambda item: (
                item[0],
                int(item[1])
                if item[0] in COLUNAS_INTEIRAS
                else CODIFICACAO_BINARIA[item[0]][item[1].strip()]
            ),
            filter(
                lambda item: item[0] not in CATEGORIAS_NOMINAIS,
                linha.items()
            )
        )
    ),
    **dict(
        map(
            lambda coluna_categoria: (
                f"{coluna_categoria[0]}_{coluna_categoria[1]}",
                int(
                    linha[coluna_categoria[0]].strip()
                    == coluna_categoria[1]
                )
            ),
            (
                (coluna, categoria)
                for coluna, categorias in CATEGORIAS_NOMINAIS.items()
                for categoria in categorias
            )
        )
    )
}

# Lê um CSV inteiro e devolve tupla de registros
ler_alunos = lambda caminho: tuple(
    map(
        transformar_linha,
        csv.DictReader(
            Path(caminho).read_text(encoding="utf-8").splitlines(),
            delimiter=DELIMITADOR
        )
    )
)

# Alunos por disciplina: {"Matemática": (...), "Português": (...)}
ALUNOS_POR_DISCIPLINA = {
    disciplina: ler_alunos(caminho)
    for disciplina, caminho in CAMINHOS_CSV.items()
}
