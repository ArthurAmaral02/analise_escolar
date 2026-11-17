from functools import reduce
import operator

# Soma dos valores, por redução com +
somar = lambda valores: reduce(operator.add, valores, 0)

# Média aritmética
media = lambda valores: (
    somar(v) / len(v) if (v := tuple(valores)) else None
)
# calcula a mediana, permite valores floats
mediana = lambda valores: (
    (
        lambda s, n: (
            s[n // 2] if n % 2 != 0
            else (s[n // 2 - 1] + s[n // 2]) / 2
        )
    )(sorted(v), len(v))
    if (v := tuple(valores)) else None
)

# Menor valor
minimo = lambda valores: (
    reduce(min, v) if (v := tuple(valores)) else None
)

# Maior valor
maximo = lambda valores: (
    reduce(max, v) if (v := tuple(valores)) else None
)

# Contagem de valores que satisfazem uma condição (soma de 1s e 0s)
contagem = lambda valores, predicado: somar(
    map(lambda valor: 1 if predicado(valor) else 0, valores)
)

# Proporção de valores que satisfazem uma condição
proporcao = lambda valores, predicado: (
    contagem(v, predicado) / len(v)
    if (v := tuple(valores)) else None
)
