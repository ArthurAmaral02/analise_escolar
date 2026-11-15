import csv
from src.organização import DELIMITADOR, CAMINHO_CSV, COLUNAS_INTEIRAS, CODIFICACAO_BINARIA, CATEGORIAS_NOMINAIS




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