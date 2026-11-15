
media = lambda valores: (
    sum(v) / len(v) if (v := tuple(valores)) else None
)

# Mediana
mediana = lambda valores: (
    (
        sorted(v)[len(v) // 2]
        if len(v) % 2 != 0
        else (
            sorted(v)[len(v) // 2 - 1]
            + sorted(v)[len(v) // 2]
        ) / 2
    )
    if (v := tuple(valores)) else None
)

# Menor valor
minimo = lambda valores: (
    min(v) if (v := tuple(valores)) else None
)

# Maior valor
maximo = lambda valores: (
    max(v) if (v := tuple(valores)) else None
)

# Contagem de valores que satisfazem uma condição
contagem = lambda valores, predicado: sum(
    1 for valor in valores if predicado(valor)
)

# Proporção de valores que satisfazem uma condição
proporcao = lambda valores, predicado: (
    contagem(v, predicado) / len(v)
    if (v := tuple(valores)) else None
)
