import math
import unittest

from src.correlacao import (
    pearson,
    spearman,
    postos,
    coeficiente,
    inclinacao,
    intercepto,
    forca_associacao,
    direcao_associacao,
    rotulo,
    matriz_correlacao,
    matriz_em_linhas,
    valores,
)
from src.dados import ler_alunos
from src.organização import CAMINHOS_CSV

TestCorrelacao = type(
    "TestCorrelacao",
    (unittest.TestCase,),
    {
        # Pearson: relação linear perfeita e sem variação
        "test_pearson_positiva_perfeita": lambda self: self.assertAlmostEqual(
            pearson([1, 2, 3], [2, 4, 6]), 1.0
        ),
        "test_pearson_negativa_perfeita": lambda self: self.assertAlmostEqual(
            pearson([1, 2, 3], [3, 2, 1]), -1.0
        ),
        "test_pearson_sem_variacao_retorna_none": lambda self: self.assertIsNone(
            pearson([1, 1, 1], [1, 2, 3])
        ),
        "test_pearson_um_par_retorna_none": lambda self: self.assertIsNone(pearson([1], [2])),

        # Postos com empates: os dois 2 ocupam as posições 2 e 3, média 2,5
        "test_postos_com_empates": lambda self: self.assertEqual(
            postos([1, 2, 2, 3]), (1.0, 2.5, 2.5, 4.0)
        ),

        # Spearman: relação monotônica não linear, perfeita para postos
        "test_spearman_monotonica_perfeita": lambda self: self.assertAlmostEqual(
            spearman([1, 2, 3, 4], [1, 4, 9, 16]), 1.0
        ),
        "test_coeficiente_escolhe_metodo": lambda self: self.assertEqual(
            coeficiente([1, 2, 3, 4], [1, 4, 9, 16], "Spearman"),
            spearman([1, 2, 3, 4], [1, 4, 9, 16]),
        ),

        # Regressão linear simples
        "test_inclinacao_e_intercepto": lambda self: self.assertEqual(
            (inclinacao([1, 2, 3], [2, 4, 6]), intercepto([1, 2, 3], [2, 4, 6])), (2.0, 0.0)
        ),

        # Classificação descritiva da força e da direção
        "test_forca_desprezivel": lambda self: self.assertEqual(forca_associacao(0.05), "desprezível"),
        "test_forca_fraca": lambda self: self.assertEqual(forca_associacao(0.25), "fraca"),
        "test_forca_moderada": lambda self: self.assertEqual(forca_associacao(0.4), "moderada"),
        "test_forca_forte_negativa": lambda self: self.assertEqual(forca_associacao(-0.8), "forte"),
        "test_forca_sem_dados": lambda self: self.assertEqual(
            forca_associacao(None), "sem dados suficientes"
        ),
        "test_direcao_negativa": lambda self: self.assertEqual(direcao_associacao(-0.1), "negativa"),

        # Rótulos: código binário vira texto; outros valores viram texto simples
        "test_rotulo_binario": lambda self: self.assertEqual(rotulo("school", 0), "GP"),
        "test_rotulo_ordinal": lambda self: self.assertEqual(rotulo("studytime", 2), "2"),

        # Matriz de correlação e conversão para linhas do gráfico
        "test_matriz_diagonal_e_simetrica": lambda self: (
            lambda registros: (
                self.assertAlmostEqual(
                    matriz_correlacao(registros, ("a", "b"), "Pearson")[("a", "a")], 1.0
                ),
                self.assertAlmostEqual(
                    matriz_correlacao(registros, ("a", "b"), "Pearson")[("a", "b")],
                    matriz_correlacao(registros, ("a", "b"), "Pearson")[("b", "a")],
                ),
            )
        )(({"a": 1, "b": 2}, {"a": 2, "b": 5}, {"a": 3, "b": 4})),
        "test_matriz_em_linhas_none_vira_nan": lambda self: self.assertTrue(
            math.isnan(
                matriz_em_linhas(
                    {("a", "a"): 1.0, ("a", "b"): None, ("b", "a"): None, ("b", "b"): 1.0},
                    ("a", "b"),
                )[0][1]
            )
        ),
        "test_matriz_em_linhas_valor_preservado": lambda self: self.assertEqual(
            matriz_em_linhas(
                {("a", "a"): 1.0, ("a", "b"): 0.5, ("b", "a"): 0.5, ("b", "b"): 1.0},
                ("a", "b"),
            ),
            [[1.0, 0.5], [0.5, 1.0]],
        ),

        # Valor de referência conhecido: G2 × G3 em Matemática, com zeros (conferido com pandas)
        "test_referencia_g2_g3_matematica_com_zeros": lambda self: self.assertEqual(
            round(
                pearson(
                    valores(ler_alunos(CAMINHOS_CSV["Matemática"]), "G2"),
                    valores(ler_alunos(CAMINHOS_CSV["Matemática"]), "G3"),
                ),
                3,
            ),
            0.905,
        ),
    },
)
