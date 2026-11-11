"""Leitura e validação dos arquivos CSV de desempenho escolar.

Esta é a camada que lida com arquivos. Ela devolve dados prontos
(tuplas de dicionários com números já convertidos), para que as
outras camadas trabalhem apenas com valores, sem depender de arquivo.
"""

import csv

DELIMITADOR = ";"

# Colunas que precisam ser números inteiros. No CSV, tudo é texto.
COLUNAS_INTEIRAS = ("G1", "G2", "G3", "absences", "failures", "studytime")


class ErroLeitura(Exception):
    """Problema ao abrir, ler ou validar um arquivo de dados."""


def _converter_linha(linha, numero_linha):
    """Devolve uma cópia da linha com as colunas numéricas convertidas.

    A linha original não é alterada: criamos um dicionário novo.
    """
    convertida = dict(linha)
    for coluna in COLUNAS_INTEIRAS:
        valor = linha[coluna]
        try:
            convertida[coluna] = int(valor)
        except ValueError:
            raise ErroLeitura(
                f"linha {numero_linha}: coluna '{coluna}' "
                f"com valor inválido: {valor!r}"
            )
    return convertida


def _verificar_cabecalho(nomes_colunas, caminho):
    """Confere se todas as colunas necessárias existem no arquivo."""
    if not nomes_colunas:
        raise ErroLeitura(f"arquivo vazio ou sem cabeçalho: {caminho}")

    faltando = [c for c in COLUNAS_INTEIRAS if c not in nomes_colunas]
    if faltando:
        raise ErroLeitura(
            f"colunas ausentes em {caminho}: {', '.join(faltando)}"
        )


def ler_alunos(caminho):
    """Lê um CSV de alunos e devolve uma tupla de dicionários validados.

    Levanta ErroLeitura se o arquivo não existir, estiver sem cabeçalho,
    não tiver as colunas necessárias ou tiver algum valor numérico inválido.
    """
    try:
        arquivo = open(caminho, newline="", encoding="utf-8")
    except FileNotFoundError:
        raise ErroLeitura(f"arquivo não encontrado: {caminho}")

    with arquivo:
        leitor = csv.DictReader(arquivo, delimiter=DELIMITADOR)
        _verificar_cabecalho(leitor.fieldnames, caminho)

        alunos = []
        for linha in leitor:
            alunos.append(_converter_linha(linha, leitor.line_num))

    return tuple(alunos)
