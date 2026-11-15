
from dados import alunos
from transformacoes import preparar_alunos, agrupar_por

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
