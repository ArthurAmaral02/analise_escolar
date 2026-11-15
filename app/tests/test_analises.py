import unittest

from src.analises import (
    resumo_geral,
    analise_por_grupo,
    analise_por_faltas,
    aprovado,
    NOMES_FAIXAS,
)
from src.dados import ler_alunos
from src.organização import CAMINHOS_CSV

# Pequeno conjunto controlado: quatro alunos, um com G3 = 0
ALUNOS_PEQUENOS = (
    {"G3": 10, "k": 1, "absences": 0},
    {"G3": 9, "k": 1, "absences": 7},
    {"G3": 12, "k": 2, "absences": 2},
    {"G3": 0, "k": 2, "absences": 12},
)

TestAnalises = type(
    "TestAnalises",
    (unittest.TestCase,),
    {
        # Regra de aprovação no limite
        "test_aprovado_no_limite": lambda self: self.assertTrue(aprovado({"G3": 10})),
        "test_reprovado_abaixo_do_limite": lambda self: self.assertFalse(aprovado({"G3": 9})),

        # Resumo geral com conjunto controlado
        "test_resumo_geral_totais": lambda self: self.assertEqual(
            (
                resumo_geral(ALUNOS_PEQUENOS)["total"],
                resumo_geral(ALUNOS_PEQUENOS)["aprovados"],
                resumo_geral(ALUNOS_PEQUENOS)["reprovados"],
            ),
            (4, 2, 2),
        ),
        "test_resumo_geral_percentual_e_media": lambda self: self.assertEqual(
            (
                resumo_geral(ALUNOS_PEQUENOS)["percentual_aprovados"],
                resumo_geral(ALUNOS_PEQUENOS)["media"],
            ),
            (0.5, 7.75),
        ),
        "test_resumo_geral_mediana_minimo_maximo": lambda self: self.assertEqual(
            (
                resumo_geral(ALUNOS_PEQUENOS)["mediana"],
                resumo_geral(ALUNOS_PEQUENOS)["minimo"],
                resumo_geral(ALUNOS_PEQUENOS)["maximo"],
            ),
            (9.5, 0, 12),
        ),

        # Análise por grupo: quantidade, média e proporção de aprovados
        "test_analise_por_grupo_valores": lambda self: self.assertEqual(
            analise_por_grupo(ALUNOS_PEQUENOS, "k", ("1", "2")),
            (("1", 2, 9.5, 0.5), ("2", 2, 6.0, 0.5)),
        ),
        "test_analise_por_grupo_respeita_ordem": lambda self: self.assertEqual(
            tuple(map(lambda linha: linha[0], analise_por_grupo(ALUNOS_PEQUENOS, "k", ("2", "1")))),
            ("2", "1"),
        ),

        # Faixas de faltas: cada aluno cai em uma faixa; a soma bate com o total
        "test_nomes_faixas_quatro": lambda self: self.assertEqual(len(NOMES_FAIXAS), 4),
        "test_analise_por_faltas_soma_total": lambda self: self.assertEqual(
            sum(map(lambda linha: linha[1], analise_por_faltas(ALUNOS_PEQUENOS))), 4
        ),

        # Arquivo real: a soma das faixas de faltas bate com o número de alunos
        "test_analise_por_faltas_arquivo_real": lambda self: self.assertEqual(
            sum(
                map(
                    lambda linha: linha[1],
                    analise_por_faltas(ler_alunos(CAMINHOS_CSV["Matemática"])),
                )
            ),
            395,
        ),
    },
)
