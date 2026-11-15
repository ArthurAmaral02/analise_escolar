import csv
from pathlib import Path

DELIMITADOR = ";"
CAMINHO_CSV = Path(__file__).resolve().parent.parent / "dados" / "student-mat.csv"

COLUNAS_INTEIRAS = (
    "age", "Medu", "Fedu", "traveltime", "studytime", "failures",
    "famrel", "freetime", "goout", "Dalc", "Walc", "health",
    "absences", "G1", "G2", "G3"
)

CODIFICACAO_BINARIA = {
    "school": {"GP": 0, "MS": 1},
    "sex": {"F": 0, "M": 1},
    "address": {"U": 0, "R": 1},
    "famsize": {"LE3": 0, "GT3": 1},
    "Pstatus": {"T": 0, "A": 1},
    "schoolsup": {"no": 0, "yes": 1},
    "famsup": {"no": 0, "yes": 1},
    "paid": {"no": 0, "yes": 1},
    "activities": {"no": 0, "yes": 1},
    "nursery": {"no": 0, "yes": 1},
    "higher": {"no": 0, "yes": 1},
    "internet": {"no": 0, "yes": 1},
    "romantic": {"no": 0, "yes": 1}
}

CATEGORIAS_NOMINAIS = {
    "Mjob": ("teacher", "health", "services", "at_home", "other"),
    "Fjob": ("teacher", "health", "services", "at_home", "other"),
    "reason": ("home", "reputation", "course", "other"),
    "guardian": ("mother", "father", "other")
}

with open(CAMINHO_CSV, newline="", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=DELIMITADOR)

    alunos = tuple(
        map(
            lambda linha: {
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
            },
            leitor
        )
    )

print(alunos[1])
print("Total de alunos:", len(alunos))
print("Total de colunas:", len(alunos[0]))