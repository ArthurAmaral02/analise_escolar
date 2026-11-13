"""Funções puras de estatística descritiva.

Regras desta camada:
- não lê arquivos, não imprime nada e não altera a entrada;
- mesma entrada sempre produz a mesma saída;
- quando não há valores para calcular, devolve None.
"""

import statistics


def media(valores):
    """Média aritmética, ou None se não houver valores."""
    valores = tuple(valores)
    if not valores:
        return None
    return sum(valores) / len(valores)


def mediana(valores):
    """Mediana, ou None se não houver valores."""
    valores = tuple(valores)
    if not valores:
        return None
    return statistics.median(valores)


def minimo(valores):
    """Menor valor, ou None se não houver valores."""
    valores = tuple(valores)
    if not valores:
        return None
    return min(valores)


def maximo(valores):
    """Maior valor, ou None se não houver valores."""
    valores = tuple(valores)
    if not valores:
        return None
    return max(valores)


def contagem(valores, predicado):
    """Quantos valores satisfazem o predicado.

    Recebe o predicado como função: a regra de seleção entra como argumento,
    e a função não precisa saber qual é.
    """
    return sum(1 for valor in valores if predicado(valor))


def proporcao(valores, predicado):
    """Fração (0 a 1) dos valores que satisfazem o predicado, ou None se vazio."""
    valores = tuple(valores)
    if not valores:
        return None
    return contagem(valores, predicado) / len(valores)
