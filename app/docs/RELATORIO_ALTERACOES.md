# Relatório de alterações — Analisador Funcional de Desempenho Escolar

**Data:** 15/11/2026
**Branch de trabalho:** `feat/correlacao-interface` (PR #1)
**Escrito para:** equipe do projeto (dupla e professora, se necessário)

---

## 1. Resumo

Nesta etapa, o projeto passou de um protótipo com uma única página e um único arquivo de dados para uma interface Streamlit completa, com:

- análise de correlação (Pearson e Spearman), implementada com a biblioteca padrão;
- análises da proposta (tempo de estudo, faltas por faixa e reprovações anteriores);
- resumo geral com aprovação;
- processamento separado de Matemática e Português;
- validação dos dados e tratamento de erros;
- código sem laços explícitos (`for`/`while`) nem `def`, usando lambdas, `map`, `filter`, `reduce` e `itertools`.

Foram feitas também decisões de projeto, registradas na seção 5.

---

## 2. Decisões tomadas

| Tema | Decisão | Quem decidiu | Observação |
|---|---|---|---|
| Interface | Streamlit (GUI), em vez de apenas terminal | Dupla | A proposta aprovada previa só terminal. Precisa ser comunicada à professora. |
| Estilo de código | Expressões (lambda, `map`, `filter`, `reduce`). Evitar `def`, `for` e `while` como comandos. Compreensões são aceitas. | Dupla | Não é proibição; é preferência de estilo. |
| Regra de aprovação | `G3 >= 10` é aprovado | Proposta (§5) | Regra analítica, não a regra oficial da escola. |
| Tratamento de `G3 = 0` | Excluído das análises por padrão, com checkbox na barra lateral para incluir | Escolha desta etapa | Em Matemática, 25 dos 38 casos com `G3 = 0` tinham `G2 > 0`, o que sugere abandono, não nota baixa. Pode ser revertido trocando o valor padrão em `app/interface/app.py`. |

---

## 3. Alterações por arquivo

### 3.1 Arquivos novos

**`app/src/correlacao.py`**
- Pearson, Spearman (postos com empates pela média), matriz de correlação, regressão linear simples (inclinação, intercepto, r²), classificação descritiva da força e da direção.
- Comparação por categorias: registros para box plot e resumo por grupo.
- Rótulos legíveis para colunas binárias (ex.: `0 → GP`).
- Validado contra `pandas.corr` nos dois arquivos.

**`app/src/analises.py`**
- `resumo_geral`: total, aprovados e reprovados (com percentuais), média, mediana, mínimo e máximo de G3.
- `analise_por_grupo`: para cada grupo, quantidade de alunos, média de G3 e proporção de aprovados.
- `analise_por_faltas`: mesma análise, por faixa de faltas (ordem definida em `organização.py`).
- `NOMES_FAIXAS` e `aprovado`.

### 3.2 Arquivos modificados

**`app/src/dados.py`**
- Antes: lia só `student-mat.csv` na importação e imprimia no console.
- Agora:
  - `ler_alunos(caminho)`: lê qualquer CSV e devolve tupla de registros. Não imprime nada.
  - `transformar_linha`: converte uma linha (inteiros, binárias e one-hot). A geração das colunas one-hot usa `chain` + `map`.
  - `carregar_disciplina(disciplina)`: carrega a disciplina escolhida. Os erros (`FileNotFoundError`, `ValueError`, `KeyError`) são tratados pela interface.
- Não há mais leitura na importação do módulo.

**`app/src/organização.py`**
- Adicionado `PASTA_DADOS` e `CAMINHOS_CSV`, com os caminhos de Matemática e Português.
- `CAMINHO_CSV` foi mantido por compatibilidade.

**`app/src/transformacoes.py`**
- `agrupar_por`: agora usa `dict(map(...))` com `set(map(...))`, sem laço.
- `remover_nota_zero` (novo): filtra alunos com `G3 != 0`, sem alterar a tupla original.
- `faixa_faltas`: `next` sobre `filter`/`map`.
- `identificar_categoria`: `next` sobre `filter`/`map`.
- `media_notas`: usa `somar` (redução com `reduce`).
- `media_por_profissao` (novo, com prefixo): base das duas funções `media_por_profissao_mae` e `media_por_profissao_pai`, que continuam com o mesmo nome e a mesma saída.

**`app/src/estatisticas.py`**
- `somar`: redução com `reduce(operator.add, ...)`. Substitui `sum`.
- `media`, `proporcao` e `contagem` usam `somar`.
- `minimo` e `maximo`: `reduce(min/max, ...)`.
- `mediana`: ordena uma vez só, dentro de uma expressão.

**`app/src/validações.py`**
- `verificar_ausentes`, `verificar_nan`: usam `contagem`.
- `verificar_one_hot`: usa `somar`.
- `import math` movido para o topo.
- As funções `verificar_limites`, `verificar_binarias` e `verificar_classificacao` não mudaram.

**`app/src/correlacao.py`** (versão final)
- `soma_quadrados` e `soma_produtos` usam `somar`.
- Matriz de correlação com `itertools.product`; geradores substituídos por `map`.

**`app/src/teste.py`**
- Antes: sequência de `print` e um `for`.
- Agora: expressões. A saída é a mesma.
- Atualizado para o novo `carregar_disciplina`.

**`app/interface/app.py`**
- Carregamento com tratamento de erro (arquivo não encontrado, valor ou coluna inesperada), sem derrubar o app.
- Painel de validação dos dados na barra lateral (valores fora da regra).
- Seletor de disciplina (Matemática e Português), processadas separadamente.
- Checkbox "Excluir alunos com G3 = 0", ligado por padrão.
- Visão geral: aprovados e reprovados com percentuais, mediana e amplitude.
- Nova página **Análises da proposta**: tempo de estudo, faltas por faixa e reprovações anteriores (tabela e gráfico).
- Nova página **Análise de correlação**: matriz (heatmap), análise individual (dispersão, linha de tendência, coeficiente, força, direção, r²) e comparação por categorias.
- Página de profissão dos pais e páginas de G1, G2 e G3 mantidas.

**`README.md`**
- Adicionada a seção "Decisões de análise". O restante do README não foi reescrito (ponto pendente).

**`docker-compose.yml`**
- Sem alteração final. Foi trocado temporariamente para `8081:8080` durante um conflito de porta e voltou para `8080:8080`.

### 3.3 Arquivos não alterados (mas relevantes)

- `app/docs/tasks/tasks.md`: plano do colega, sem alteração (checkboxes não marcados).
- `app/docs/planilha_format/novas implementações.md`: dicionário de dados, sem alteração.
- `Contexto/proposta_analisador_funcional_desempenho_escolar.md`: sem alteração (aguarda revisão, ver seção 6).
- `GUIA.md`: sem alteração e fora do git.

---

## 4. Controle de versão

- **Branch:** `feat/correlacao-interface`, criada a partir de `main`.
- **Commit `2d56105`:** correlação, seleção de disciplina, leitura separada de `dados.py`, `agrupar_por` e `teste.py`. Não inclui as alterações posteriores (ver abaixo).
- **PR #1:** https://github.com/ArthurAmaral02/analise_escolar/pull/1
- **Alterações na árvore de trabalho, ainda sem commit:**
  - `estatisticas.py`, `validações.py`, `analises.py`, `transformacoes.py`, `correlacao.py`, `teste.py`, `dados.py` (versões com `reduce` e `map`);
  - `interface/app.py` (análises da proposta, validação, erros, resumo geral);
  - `README.md` (decisões);
  - `docs/RELATORIO_ALTERACOES.md` (este relatório).
- **Não versionados:** `GUIA.md` e `.venv/`. Recomenda-se adicionar `.venv/` ao `.gitignore`.

---

## 5. Verificação realizada

| Verificação | Resultado |
|---|---|
| Pearson e Spearman comparados com `pandas.corr` (G1, G2, G3, studytime, absences, failures, schoolsup) | Iguais, nos dois arquivos |
| Resumo geral comparado com pandas (total, aprovados, percentual, média, mediana) | Iguais, nos dois arquivos |
| Faixas de faltas: soma das contagens | Igual ao total de alunos |
| Validações (`verificar_ausentes`, `verificar_limites`, `verificar_binarias`, `verificar_one_hot`, `verificar_nan`) | Idênticas às originais do git, nos dois arquivos |
| Erro de arquivo inexistente | `FileNotFoundError` capturado pela interface |
| Erro de coluna inesperada | `KeyError` capturado pela interface |
| Estatísticas (média, mediana, mínimo, máximo, contagem, proporção) | Comparadas com built-ins e `statistics.median` em 2000 listas aleatórias |
| Saídas de 39 funções antes e depois da conversão para expressões | Todas iguais |
| Interface Streamlit (`AppTest`): todas as páginas, nas duas disciplinas, com e sem o filtro de zeros | Sem exceções |

**Números de referência (Matemática e Português):**

| | Matemática | Português |
|---|---|---|
| Registros no arquivo | 395 | 649 |
| `G3 = 0` | 38 | 15 |
| Considerados (sem `G3 = 0`) | 357 | 634 |
| Aprovados (sem `G3 = 0`) | 265 (74,2%) | 549 (86,6%) |
| Correlação G2 × G3 de Pearson (com zeros → sem zeros) | 0,905 → 0,966 | — |

**Ambiente de teste:** Python 3.10 (sistema), com pandas 2.3.3, streamlit 1.65.0, plotly 7.1.0 e scipy (apenas para comparação). Fora do projeto. O Docker usa Python 3.11.

---

## 6. Pendências

**Documentação e proposta**
1. Revisar a proposta aprovada: trocar o exemplo com `def` por lambdas, registrar a interface (Streamlit) e a regra de estilo, e comunicar a mudança à professora.
2. Atualizar `tasks.md` (marcar o que já está feito) e o GUIA, que ainda diz "terminal, sem GUI".
3. Reescrever o `README.md` completo: como rodar, o que cada arquivo faz, variáveis, limitações e como rodar testes.

**Testes e qualidade**
4. Escrever os testes `unittest` (pasta `tests/`). Os testes podem ser criados sem `def`, com `type(...)` e lambdas no dicionário da classe.
5. Trocar `use_container_width` por `width="stretch"` (aviso de depreciação do Streamlit).
6. Mensagem de `KeyError` pouco clara (mostra só a chave). Pode ser melhorada.

**Interface e execução**
7. `app/interface/app.py` ainda usa comandos (`try/except`, `if/elif` para páginas e chamadas `st.*`). Trocar só o que for possível; o restante é próprio do Streamlit.
8. Dockerfile: `CMD` ainda é `tail -f`. Para subir o app direto, usar `streamlit run interface/app.py --server.address=0.0.0.0 --server.port=8080`.
9. Após alterar módulos, reiniciar o Streamlit dentro do container (`docker compose restart analise` e novo `streamlit run`).

**Limpeza**
10. Remover o arquivo de lock do LibreOffice (`app/dados/.~lock.student-mat.csv#`), que está versionado.
11. Adicionar `.venv/` ao `.gitignore`.
12. Decidir sobre `app/src/teste.py` (rascunho; pode ser apagado).

**Commit**
13. Commitar e publicar as alterações da árvore de trabalho no PR #1 (ou em um novo PR), depois de revisão.

**Decisão aberta**
14. Confirmar com a equipe o padrão de `G3 = 0` (excluído por padrão). Se a decisão mudar, basta trocar o valor padrão do checkbox em `app/interface/app.py`.

---

## 7. Como rodar

```bash
cd analise_escolar
python3 -m venv .venv && source .venv/bin/activate
pip install -r app/requirements.txt
cd app/interface
streamlit run app.py --server.port=8080
```

Ou com Docker (porta 8080 precisa estar livre):

```bash
docker compose up -d --build
docker compose exec -d analise streamlit run interface/app.py --server.address=0.0.0.0 --server.port=8080
```
