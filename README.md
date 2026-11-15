# Analisador Funcional de Desempenho Escolar

Programa em Python que resume e compara o desempenho de alunos do ensino secundário em Portugal, usando o dataset **Student Performance** (UCI Machine Learning Repository). O foco do projeto é a **programação funcional**: funções puras, imutabilidade, composição e expressões no lugar de laços e comandos.

Os dados são observacionais. As relações encontradas são associações e **não** demonstram causa e efeito.

---

## Requisitos

- Python 3.10 ou superior (o Docker usa 3.11)
- Dependências em `app/requirements.txt`: `pandas`, `streamlit`, `plotly`

Os cálculos de `src/` usam apenas a biblioteca padrão. As dependências externas são usadas só na interface.

---

## Como rodar

### Opção 1: local

```bash
cd analise_escolar
python3 -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt

cd app/interface
streamlit run app.py --server.port=8080
```

Abra `http://localhost:8080` no navegador.

### Opção 2: Docker

```bash
cd analise_escolar
docker compose up -d --build
```

A interface sobe sozinha em `http://localhost:8080`. A porta 8080 do computador precisa estar livre.

---

## Estrutura do projeto

```
analise_escolar/
├── app/
│   ├── dados/                 CSVs de Matemática e Português (separador ;)
│   ├── src/                   código funcional (núcleo do projeto)
│   │   ├── organização.py     constantes: variáveis, faixas, limites, caminhos
│   │   ├── dados.py           leitura dos CSVs
│   │   ├── validações.py      verificação de limites, binárias, one-hot, ausentes e NaN
│   │   ├── transformacoes.py  classificação, faixas de faltas, agrupamento
│   │   ├── estatisticas.py    média, mediana, mínimo, máximo, contagem, proporção
│   │   ├── analises.py        resumo geral e análises por grupo
│   │   ├── correlacao.py      Pearson, Spearman, regressão linear simples
│   │   └── teste.py           rascunho de execução (pode ser removido)
│   ├── interface/app.py       interface Streamlit
│   ├── tests/                 testes automatizados (unittest)
│   ├── docs/                  documentação auxiliar e relatório de alterações
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

### Módulos de `src/`

| Módulo | Responsabilidade |
|---|---|
| `organização.py` | Listas de variáveis, limite de aprovação (10), faixas de faltas, codificação das binárias e caminhos dos arquivos |
| `dados.py` | `ler_alunos(caminho)` lê um CSV e devolve uma tupla de registros. `carregar_disciplina(nome)` escolhe o arquivo pelo nome da disciplina |
| `validações.py` | Verifica valores fora dos limites, binárias inválidas, grupos one-hot sem exatamente uma marca, ausentes e NaN |
| `transformacoes.py` | `classificar_resultado`, `faixa_faltas`, `agrupar_por`, `remover_nota_zero`, profissão dos pais |
| `estatisticas.py` | Funções de cálculo sobre sequências de números (retornam `None` quando a entrada é vazia) |
| `analises.py` | `resumo_geral` (aprovação, média, mediana) e `analise_por_grupo` (quantidade, média de G3, percentual de aprovados) |
| `correlacao.py` | Pearson, Spearman (com postos e empates), matriz de correlação, regressão linear simples e descrição da força |

Todas as funções de `src/` são lambdas ou expressões. Não há `def`, `for` ou `while` como comandos.

---

## Dados

Dois arquivos, analisados **separadamente**:

| Arquivo | Disciplina | Registros |
|---|---|---|
| `app/dados/student-mat.csv` | Matemática | 395 |
| `app/dados/student-por.csv` | Português | 649 |

Formato: separador `;`, com 33 colunas originais. As colunas nominais (`Mjob`, `Fjob`, `reason`, `guardian`) viram colunas one-hot, o que dá 46 colunas no total.

Variáveis principais:

| Variável | Significado |
|---|---|
| `G1`, `G2`, `G3` | Notas do 1º período, do 2º período e final (0 a 20). `G3` é a principal |
| `studytime` | Tempo semanal de estudo: 1 (<2h), 2 (2–5h), 3 (5–10h), 4 (>10h) |
| `absences` | Número de faltas (0 a 75) |
| `failures` | Reprovações **anteriores** (não é o resultado atual) |

O dicionário completo das variáveis está em `app/docs/planilha_format/novas implementações.md`.

---

## Decisões de análise

- **Aprovação:** `G3 >= 10` é aprovado; `G3 < 10` é reprovado. É uma regra analítica do projeto, não a regra oficial da escola.
- **G3 = 0:** excluído das análises por padrão (checkbox na barra lateral da interface). Em Matemática, 25 dos 38 alunos com G3 = 0 tinham G2 > 0, o que sugere abandono ou não conclusão, não nota baixa. Para incluí-los, desmarque a opção.
- **Interface:** Streamlit. A proposta original previa apenas terminal; a mudança está registrada no relatório de alterações.
- **Análises descritivas:** diferenças entre grupos e correlações não comprovam causa e efeito.

---

## Testes

Os testes ficam em `app/tests/` e usam apenas `unittest`. Cobrem `estatisticas`, `transformacoes`, `validações`, `correlacao`, `analises` e `dados`, incluindo valores de borda (G3 = 9 e 10, faixas de faltas) e entradas que não podem ser alteradas.

```bash
cd analise_escolar/app
python -m unittest discover -s tests -v
```

Com Docker:

```bash
docker compose exec analise python -m unittest discover -s tests -v
```

---

## Limitações

- Os dados são de duas escolas de Portugal e não devem ser generalizados para outros estudantes.
- `failures` mede reprovações anteriores e não substitui `G3` para avaliar o resultado atual.
- Os dois arquivos não têm identificador de aluno, então não há junção entre disciplinas.
- Pearson e Spearman medem associação. Para variáveis binárias e ordinais, a interpretação é descritiva.
- A linha de tendência é a regressão linear simples, mesmo quando o coeficiente exibido é Spearman.
