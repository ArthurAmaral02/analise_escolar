import unittest

from src.estatisticas import media, mediana, minimo, maximo, contagem, proporcao, somar

# Testes escritos como expressões: cada método é uma lambda dentro da classe.
TestEstatisticas = type(
    "TestEstatisticas",
    (unittest.TestCase,),
    {
        "test_media_caso_comum": lambda self: self.assertEqual(media([10, 12, 14]), 12),
        "test_media_lista_vazia_retorna_none": lambda self: self.assertIsNone(media([])),
        "test_media_numeros_pares": lambda self: self.assertEqual(media([1, 2, 3, 4]), 2.5),
        "test_media_nao_altera_entrada": lambda self: (
            lambda lista: (media(lista), self.assertEqual(lista, [10, 12, 14]))
        )([10, 12, 14]),

        "test_mediana_impar": lambda self: self.assertEqual(mediana([10, 12, 14]), 12),
        "test_mediana_par": lambda self: self.assertEqual(mediana([1, 2, 3, 4]), 2.5),
        "test_mediana_lista_vazia_retorna_none": lambda self: self.assertIsNone(mediana([])),
        "test_mediana_nao_ordena_entrada": lambda self: (
            lambda lista: (mediana(lista), self.assertEqual(lista, [3, 1, 2]))
        )([3, 1, 2]),

        "test_minimo_e_maximo": lambda self: self.assertEqual(
            (minimo([3, 1, 2]), maximo([3, 1, 2])), (1, 3)
        ),
        "test_minimo_maximo_vazios_retornam_none": lambda self: self.assertEqual(
            (minimo([]), maximo([])), (None, None)
        ),

        "test_somar_lista": lambda self: self.assertEqual(somar([1, 2, 3]), 6),
        "test_somar_vazio_e_zero": lambda self: self.assertEqual(somar([]), 0),

        "test_contagem_com_predicado": lambda self: self.assertEqual(
            contagem([1, 2, 3], lambda x: x > 1), 2
        ),
        "test_contagem_vazia_e_zero": lambda self: self.assertEqual(
            contagem([], lambda x: x > 1), 0
        ),

        "test_proporcao_caso_comum": lambda self: self.assertEqual(
            proporcao([1, 2, 3, 4], lambda x: x > 2), 0.5
        ),
        "test_proporcao_vazia_retorna_none": lambda self: self.assertIsNone(
            proporcao([], lambda x: x > 2)
        ),
    },
)
