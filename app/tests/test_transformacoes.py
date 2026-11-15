import unittest

from src.transformacoes import (
    classificar_resultado,
    faixa_faltas,
    remover_nota_zero,
    agrupar_por,
    adicionar_faixa_faltas,
    notas_validas,
    identificar_categoria,
    media_notas,
    media_por_profissao_mae,
)

TestTransformacoes = type(
    "TestTransformacoes",
    (unittest.TestCase,),
    {
        # Regra de aprovação: G3 = 10 aprovado, G3 = 9 reprovado (limite)
        "test_classificar_no_limite_aprovado": lambda self: self.assertEqual(
            classificar_resultado(10), "Aprovado"
        ),
        "test_classificar_abaixo_do_limite_reprovado": lambda self: self.assertEqual(
            classificar_resultado(9), "Reprovado"
        ),

        # Faixas de faltas: valores de borda de cada faixa
        "test_faixa_zero_faltas": lambda self: self.assertEqual(faixa_faltas(0), "0 faltas"),
        "test_faixa_limite_inferior": lambda self: self.assertEqual(faixa_faltas(1), "1 a 5 faltas"),
        "test_faixa_limite_superior": lambda self: self.assertEqual(faixa_faltas(5), "1 a 5 faltas"),
        "test_faixa_seis_faltas": lambda self: self.assertEqual(faixa_faltas(6), "6 a 10 faltas"),
        "test_faixa_mais_de_dez": lambda self: self.assertEqual(faixa_faltas(11), "mais de 10 faltas"),
        "test_faixa_fora_do_intervalo_retorna_none": lambda self: self.assertIsNone(faixa_faltas(-1)),

        # Remoção de G3 = 0 sem alterar a entrada
        "test_remover_nota_zero": lambda self: self.assertEqual(
            remover_nota_zero(({"G3": 0}, {"G3": 5})), ({"G3": 5},)
        ),
        "test_remover_nota_zero_nao_altera_entrada": lambda self: (
            lambda registros: (
                remover_nota_zero(registros),
                self.assertEqual(len(registros), 2),
            )
        )(({"G3": 0}, {"G3": 5})),

        # Validação de notas: aceita inteiros de 0 a 20
        "test_notas_validas_remove_fora_da_faixa": lambda self: self.assertEqual(
            notas_validas(({"G3": 21}, {"G3": 7}, {"G3": "x"})), ({"G3": 7},)
        ),

        # Agrupamento: um grupo por valor, sem perder registros
        "test_agrupar_por_mantem_todos_os_registros": lambda self: self.assertEqual(
            (
                len(agrupar_por(({"k": 1}, {"k": 2}, {"k": 1}), "k")[1]),
                len(agrupar_por(({"k": 1}, {"k": 2}, {"k": 1}), "k")[2]),
            ),
            (2, 1),
        ),

        # Adiciona a faixa sem alterar o registro original
        "test_adicionar_faixa_nao_altera_original": lambda self: (
            lambda aluno: (
                adicionar_faixa_faltas(aluno)["faixa_faltas"],
                self.assertEqual(aluno, {"absences": 7}),
            )
        )({"absences": 7}),
        "test_adicionar_faixa_valor_correto": lambda self: self.assertEqual(
            adicionar_faixa_faltas({"absences": 7})["faixa_faltas"], "6 a 10 faltas"
        ),

        # Profissão a partir das colunas one-hot
        "test_identificar_categoria_one_hot": lambda self: self.assertEqual(
            identificar_categoria({"Mjob_teacher": 0, "Mjob_health": 1}, "Mjob_"), "health"
        ),
        "test_identificar_categoria_sem_marca": lambda self: self.assertEqual(
            identificar_categoria({"Mjob_teacher": 0}, "Mjob_"), "desconhecido"
        ),

        # Média de G3 por grupo
        "test_media_notas_grupo": lambda self: self.assertEqual(
            media_notas(({"G3": 10}, {"G3": 12})), 11
        ),
        "test_media_notas_vazio_retorna_zero": lambda self: self.assertEqual(media_notas([]), 0),

        "test_media_por_profissao_mae": lambda self: self.assertEqual(
            media_por_profissao_mae((
                {"Mjob_teacher": 1, "Mjob_health": 0, "G3": 10},
                {"Mjob_teacher": 1, "Mjob_health": 0, "G3": 14},
                {"Mjob_teacher": 0, "Mjob_health": 1, "G3": 6},
            )),
            {"health": 6, "teacher": 12},
        ),
    },
)
