"""Transformações puras sobre registros de alunos.

Regras desta camada:
- nenhuma função altera a entrada: sempre devolve coleções ou dicionários novos;
- nenhuma função lê arquivos ou imprime nada;
- a regra de aprovação e as faixas de faltas ficam aqui, documentadas.
"""

from functools import reduce

# Regra analítica da proposta: G3 >= 10 é aprovação.
NOTA_MINIMA_APROVACAO = 10

# Faixas de faltas (inclusivas). Máximo None significa "sem limite".
FAIXAS_FALTAS = (
    ("0 faltas", 0, 0),
    ("1 a 5 faltas", 1, 5),
    ("6 a 10 faltas", 6, 10),
    ("mais de 10 faltas", 11, None),
)


def compor(*funcoes):
    """Devolve uma função que aplica as funções em sequência, da esquerda para a direita."""
    return lambda entrada: reduce(lambda acumulado, funcao: funcao(acumulado), funcoes, entrada)


def mapear(funcao):
    """Transforma uma função de um registro em uma função de coleção.

    Útil para compor: mapear(f) aplicado a uma coleção devolve uma tupla nova.
    """
    return lambda registros: tuple(map(funcao, registros))


def nota_valida(aluno):
    """True se G3 é um inteiro entre 0 e 20."""
    nota = aluno.get("G3")
    return isinstance(nota, int) and 0 <= nota <= 20


def notas_validas(alunos):
    """Mantém só os alunos com G3 válida. Não inclui G3 = 0 como inválida."""
    return tuple(filter(nota_valida, alunos))


def classificar_resultado(nota):
    """'Aprovado' ou 'Reprovado' a partir de G3."""
    return "Aprovado" if nota >= NOTA_MINIMA_APROVACAO else "Reprovado"


def faixa_faltas(faltas):
    """Rótulo da faixa de faltas a que o número pertence, ou None se fora de todas."""
    faixa = next(
        filter(
            lambda f: f[1] <= faltas and (f[2] is None or faltas <= f[2]),
            FAIXAS_FALTAS,
        ),
        None,
    )
    return faixa[0] if faixa else None


def adicionar_resultado(aluno):
    """Cópia do aluno com a chave 'resultado' acrescentada."""
    return {**aluno, "resultado": classificar_resultado(aluno["G3"])}


def adicionar_faixa_faltas(aluno):
    """Cópia do aluno com a chave 'faixa_faltas' acrescentada."""
    return {**aluno, "faixa_faltas": faixa_faltas(aluno["absences"])}


def agrupar_por(registros, coluna):
    """Dicionário {valor: tupla de registros}, com os valores em ordem.

    Cada grupo é uma tupla nova; a lista de entrada não muda.
    """
    valores = tuple(sorted({registro[coluna] for registro in registros}))
    return {
        valor: tuple(filter(lambda registro: registro[coluna] == valor, registros))
        for valor in valores
    }


# Pipeline de preparação: valida, classifica e acrescenta a faixa de faltas.
preparar_alunos = compor(
    notas_validas,
    mapear(adicionar_resultado),
    mapear(adicionar_faixa_faltas),
)
