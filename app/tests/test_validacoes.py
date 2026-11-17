import unittest

from src.dados import ler_alunos
from src.organização import CAMINHOS_CSV
from src.validações import (
    verificar_ausentes,
    verificar_limites,
    verificar_binarias,
    verificar_one_hot,
    verificar_nan,
)

# Um registro real, com todas as colunas, usado como base para os casos de teste
REGISTRO = ler_alunos(CAMINHOS_CSV["Matemática"])[0]

# Conta os registros reprovados na regra de uma coluna
fora_da_regra = lambda resultado, coluna: len(
    dict(resultado)[coluna]
)

TestValidacoes = type(
    "TestValidacoes",
    (unittest.TestCase,),
    {
        # Limites: G3 acima de 20 deve ser detectado
        "test_limites_detecta_g3_acima_de_20": lambda self: self.assertEqual(
            fora_da_regra(verificar_limites((dict(REGISTRO, G3=21),)), "G3"), 1
        ),
        "test_limites_aceita_g3_no_limite": lambda self: self.assertEqual(
            fora_da_regra(verificar_limites((dict(REGISTRO, G3=20),)), "G3"), 0
        ),

        # Binárias: qualquer valor diferente de 0 e 1 deve ser detectado
        "test_binarias_detecta_valor_invalido": lambda self: self.assertEqual(
            fora_da_regra(verificar_binarias((dict(REGISTRO, schoolsup=2),)), "schoolsup"), 1
        ),
        "test_binarias_registro_real_sem_erro": lambda self: self.assertEqual(
            sum(map(lambda par: len(par[1]), verificar_binarias((REGISTRO,)))), 0
        ),

        # One-hot: cada grupo deve ter exatamente uma categoria marcada
        "test_one_hot_detecta_grupo_sem_marca": lambda self: self.assertEqual(
            fora_da_regra(
                verificar_one_hot((dict(REGISTRO, **{k: 0 for k in REGISTRO if k.startswith("Mjob_")}),)),
                "Mjob",
            ),
            1,
        ),
        "test_one_hot_registro_real_sem_erro": lambda self: self.assertEqual(
            sum(map(lambda par: len(par[1]), verificar_one_hot((REGISTRO,)))), 0
        ),

        # Ausentes e NaN: o arquivo real não tem nenhum
        "test_ausentes_arquivo_real_zero": lambda self: self.assertEqual(
            sum(map(lambda par: par[1], verificar_ausentes(ler_alunos(CAMINHOS_CSV["Matemática"])))), 0
        ),
        "test_nan_arquivo_real_zero": lambda self: self.assertEqual(
            sum(map(lambda par: par[1], verificar_nan(ler_alunos(CAMINHOS_CSV["Matemática"])))), 0
        ),
    },
)
