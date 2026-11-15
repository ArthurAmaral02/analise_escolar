from src.dados import carregar_disciplina
from src.transformacoes import preparar_alunos, agrupar_por
from src.validações import verificar_binarias

alunos = carregar_disciplina("Matemática")

# Prepara os registros e agrupa por resultado e por faixa de faltas
alunos_preparados = preparar_alunos(alunos)
resultados = agrupar_por(alunos_preparados, "resultado")
faltas = agrupar_por(alunos_preparados, "faixa_faltas")

# Cada linha é uma expressão; map(print, ...) executa os prints
tuple(
    map(
        print,
        (
            "Aprovados: " + str(len(resultados.get("Aprovado", ()))),
            "Reprovados: " + str(len(resultados.get("Reprovado", ()))),
            "\nAlunos por faixa de faltas:",
        )
        + tuple(map(lambda item: f"{item[0]}: {len(item[1])}", faltas.items()))
        + (
            "Quantidade de variáveis: " + str(len(alunos[0])),
            "\nVariáveis disponíveis:",
            str(tuple(alunos[0].keys())),
            "\n\n\n\n",
            str(verificar_binarias(alunos)),
        )
    )
)
