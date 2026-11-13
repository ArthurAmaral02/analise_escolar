import csv
from pathlib import Path
from functools import reduce

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

#print(alunos)

quantidade_alunos = reduce(lambda acumulador, aluno: acumulador + 1, alunos, 0)

print(quantidade_alunos)

total_q1 = reduce(
    lambda acumulador, aluno: acumulador + aluno["G1"],
    alunos,
    0
) / quantidade_alunos

total_q2 = (
    lambda valor: valor / quantidade_alunos
)(
    reduce(
        lambda acumulador, aluno: acumulador + aluno["G1"],
        alunos,
        0
    )
)

print(total_q2)



def teste():
    teste_num = [1,2,3,4,5,6,7,8,9]
    q = 9
    probabilidade = reduce(lambda m, x: m + (x/q), teste_num, 0)
    print(probabilidade)

