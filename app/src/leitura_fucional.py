import csv
from pathlib import Path

DELIMITADOR = ";"
CAMINHO_CSV = Path(__file__).resolve().parent.parent / "dados" / "student-mat.csv"
# Colunas que precisam ser números inteiros. No CSV, tudo é texto.
COLUNAS_INTEIRAS = ("G1", "G2", "G3", "absences", "failures", "studytime")

with open(CAMINHO_CSV, newline="", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=DELIMITADOR)

    alunos = tuple(
        map(
            lambda linha: dict(
                map(
                    lambda item: (
                        item[0],
                        int(item[1]) if item[0] in COLUNAS_INTEIRAS else item[1]
                    ),
                    linha.items()
                )
            ),
            leitor
        )
    )

print(alunos[1])