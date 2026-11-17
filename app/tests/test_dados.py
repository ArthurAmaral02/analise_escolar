import csv
import unittest
from pathlib import Path

from src.dados import ler_alunos, carregar_disciplina, transformar_linha
from src.organização import CAMINHOS_CSV

# Primeira linha crua do CSV de Matemática (texto, como o DictReader entrega)
LINHA_BRUTA = next(
    csv.DictReader(
        Path(CAMINHOS_CSV["Matemática"]).read_text(encoding="utf-8").splitlines(),
        delimiter=";",
    )
)

TestDados = type(
    "TestDados",
    (unittest.TestCase,),
    {
        # Tamanho dos arquivos reais (conforme o dicionário de dados)
        "test_matematica_395_alunos": lambda self: self.assertEqual(
            len(ler_alunos(CAMINHOS_CSV["Matemática"])), 395
        ),
        "test_portugues_649_alunos": lambda self: self.assertEqual(
            len(ler_alunos(CAMINHOS_CSV["Português"])), 649
        ),

        # 33 colunas originais, com as 4 nominais substituídas por 17 colunas one-hot
        "test_registro_tem_46_colunas": lambda self: self.assertEqual(
            len(ler_alunos(CAMINHOS_CSV["Matemática"])[0]), 46
        ),

        # Tipos: notas e faltas são inteiros, não texto
        "test_notas_sao_inteiros": lambda self: self.assertTrue(
            all(
                map(
                    lambda aluno: isinstance(aluno["G1"], int)
                    and isinstance(aluno["G2"], int)
                    and isinstance(aluno["G3"], int),
                    ler_alunos(CAMINHOS_CSV["Matemática"]),
                )
            )
        ),

        # Carregar pela disciplina é o mesmo que ler o caminho
        "test_carregar_disciplina_igual_ao_caminho": lambda self: self.assertEqual(
            carregar_disciplina("Português"),
            ler_alunos(CAMINHOS_CSV["Português"]),
        ),

        # Erro de arquivo inexistente é explícito
        "test_arquivo_inexistente_levanta_erro": lambda self: self.assertRaises(
            FileNotFoundError, lambda: ler_alunos("nao_existe.csv")
        ),

        # Valor binário desconhecido na linha crua é reportado como KeyError
        "test_transformar_linha_valor_invalido": lambda self: self.assertRaises(
            KeyError,
            lambda: transformar_linha({**LINHA_BRUTA, "schoolsup": "talvez"}),
        ),
        "test_transformar_linha_crua_valida": lambda self: self.assertEqual(
            transformar_linha(LINHA_BRUTA)["G3"], 6
        ),
    },
)
