
from src.dados import ALUNOS_POR_DISCIPLINA

alunos = ALUNOS_POR_DISCIPLINA["Matemática"]
from src.transformacoes import preparar_alunos,agrupar_por
from src.validações import verificar_binarias

# Prepara os registros
alunos_preparados = preparar_alunos(alunos)

# Agrupa alunos por resultado
resultados = agrupar_por(alunos_preparados, "resultado")

print("Aprovados:", len(resultados.get("Aprovado", ())))
print("Reprovados:", len(resultados.get("Reprovado", ())))

# Agrupa alunos por faixa de faltas
faltas = agrupar_por(alunos_preparados, "faixa_faltas")

print("\nAlunos por faixa de faltas:")

for faixa, grupo in faltas.items():
    print(f"{faixa}: {len(grupo)}")


quantidade_e_chaves = lambda: (
    print("Quantidade de variáveis:", len(alunos[0])),
    print("\nVariáveis disponíveis:"),
    print(tuple(alunos[0].keys()))
)

quantidade_e_chaves()

espaco = lambda: (print("\n\n\n\n"))

espaco()

print(verificar_binarias(alunos))