# Relatório de alterações — Analisador Funcional de Desempenho Escolar

**Data:** 15/11/2026
**Branch:** `feat/correlacao-interface` (PR #1)
**Escrito para:** equipe do projeto (dupla e professora, se necessário)

---

## 1. Resumo

O projeto passou de um protótipo com uma página e um único arquivo de dados para uma interface Streamlit completa, com:

- análise de correlação (Pearson e Spearman), implementada com a biblioteca padrão;
- análises da proposta (tempo de estudo, faltas por faixa e reprovações anteriores);
- resumo geral com aprovação;
- processamento separado de Matemática e Português;
- validação dos dados e tratamento de erros;
- código de `src/` em expressões: sem `def`, `for` ou `while` como comandos, usando `lambda`, `map`, `filter`, `reduce` e `itertools`;
- 81 testes automatizados com `unittest`;
- Docker subindo a interface sozinho;
- README reescrito e documentação atualizada.

---

## 2. Decisões tomadas

| Tema | Decisão | Quem decidiu | Observação |
|---|---|---|---|
| Interface | Streamlit, como complemento ao terminal | Dupla | Registrada na revisão 2 da proposta (seção 15). A avaliação foca em `src/`. |
| Estilo de código | Expressões (`lambda`, `map`, `filter`, `reduce`). Sem `def`, `for` e `while` como comandos. Compreensões são aceitas. | Dupla | Registrado na seção 7 da proposta. |
| Regra de aprovação | `G3 >= 10` é aprovado | Proposta (§5) | Regra analítica, não a regra oficial da escola. |
| Tratamento de `G3 = 0` | Excluído das análises por padrão, com checkbox na barra lateral para incluir | Escolha desta etapa | Em Matemática, 25 dos 38 casos com `G3 = 0` tinham `G2 > 0`, o que sugere abandono, não nota baixa. Para trocar o padrão, altere `value=True` no checkbox em `app/interface/app.py`. |

---

## 3. Alterações por arquivo

### 3.1 Arquivos novos

**`app/src/correlacao.py`**
- Pearson, Spearman (postos com empates pela média), matriz de correlação, regressão linear simples (inclinação, intercepto, r²), descrição da força e da direção.
- Comparação por categorias: registros para box plot e resumo por grupo.
- Rótulos legíveis para colunas binárias (ex.: `0 → GP`).
- Validado contra `pandas.corr` nos dois arquivos.

**`app/src/analises.py`**
- `resumo_geral`: total, aprovados e reprovados (com percentuais), média, mediana, mínimo e máximo de G3.
- `analise_por_grupo`: para cada grupo, quantidade de alunos, média de G3 e proporção de aprovados.
- `analise_por_faltas`: mesma análise, por faixa de faltas (ordem definida em `organização.py`).

**`app/tests/`** (6 arquivos, 81 testes)
- `test_estatisticas.py`, `test_transformacoes.py`, `test_validacoes.py`, `test_correlacao.py`, `test_analises.py`, `test_dados.py`.
- Cada teste é uma lambda dentro de uma classe criada com `type(...)`, sem `def`.
- Cobrem valores de borda (G3 = 9 e 10, faixas de faltas), entradas que não podem ser alteradas e um valor de referência de correlação.

### 3.2 Arquivos modificados

**`app/src/dados.py`**
- Antes: lia só `student-mat.csv` na importação e imprimia no console.
- Agora:
  - `ler_alunos(caminho)`: lê qualquer CSV e devolve uma tupla de registros. Não imprime nada.
  - `transformar_linha`: converte uma linha (inteiros, binárias e one-hot). As colunas one-hot usam `chain` + `map`.
  - `carregar_disciplina(disciplina)`: carrega a disciplina escolhida. Os erros (`FileNotFoundError`, `ValueError`, `KeyError`) são tratados pela interface.
- Não há leitura na importação do módulo.

**`app/src/organização.py`**
- Adicionados `PASTA_DADOS` e `CAMINHOS_CSV`, com os caminhos de Matemática e Português.
- `CAMINHO_CSV` foi mantido por compatibilidade.

**`app/src/transformacoes.py`**
- `agrupar_por`: `dict(map(...))` com `set(map(...))`, sem laço.
- `remover_nota_zero` (novo): filtra alunos com `G3 != 0`, sem alterar a tupla original.
- `faixa_faltas` e `identificar_categoria`: `next` sobre `filter`/`map`.
- `media_notas`: usa `somar` (redução com `reduce`).
- `media_por_profissao` (novo): base das funções `media_por_profissao_mae` e `media_por_profissao_pai`, que mantêm o nome e a saída.

**`app/src/estatisticas.py`**
- `somar`: redução com `reduce(operator.add, ...)`, no lugar de `sum`.
- `media`, `proporcao` e `contagem` usam `somar`.
- `minimo` e `maximo`: `reduce(min/max, ...)`.
- `mediana`: ordena uma vez só, dentro de uma expressão.

**`app/src/validações.py`**
- `verificar_ausentes` e `verificar_nan` usam `contagem`; `verificar_one_hot` usa `somar`.
- `import math` movido para o topo.
- `verificar_limites`, `verificar_binarias` e `verificar_classificacao` não mudaram.

**`app/src/correlacao.py`**
- `soma_quadrados` e `soma_produtos` usam `somar`.
- Matriz de correlação com `itertools.product`; geradores substituídos por `map`.

**`app/src/teste.py`**
- Antes: sequência de `print` e um `for`. Agora: expressões, com a mesma saída.

**`app/interface/app.py`**
- Tratamento de erro no carregamento (arquivo não encontrado, valor ou coluna inesperada), sem derrubar o app.
- Painel de validação dos dados na barra lateral.
- Seletor de disciplina (Matemática e Português), processadas separadamente.
- Checkbox "Excluir alunos com G3 = 0", ligado por padrão.
- Visão geral com aprovados e reprovados (quantidade e percentual), mediana e amplitude.
- Página **Análises da proposta** (tempo de estudo, faltas por faixa e reprovações anteriores).
- Página **Análise de correlação** (matriz, análise individual e comparação por categorias).
- Páginas de profissão dos pais e de G1, G2 e G3 mantidas.

**`app/Dockerfile`**
- `CMD` trocado de `tail -f` para `streamlit run interface/app.py --server.address=0.0.0.0 --server.port=8080`. O container sobe a interface sozinho.

**`README.md`**
- Reescrito por completo: requisitos, como rodar (local e Docker), estrutura, módulos de `src/`, dados, decisões, testes e limitações.

**`app/docs/tasks/tasks.md`**
- Itens já implementados marcados como concluídos. Interpretação e conclusão continuam em aberto.

**`.gitignore`**
- Incluídos `.venv/` e arquivos de lock do LibreOffice (`.~lock.*#`).

**`app/dados/.~lock.student-mat.csv#`**
- Removido do versionamento (`git rm --cached`). Continua no disco, porque pertence a outra sessão.

**`docker-compose.yml`**
- Sem alteração final. Foi trocado temporariamente para `8081:8080` durante um conflito de porta e voltou para `8080:8080`.

### 3.3 Fora do repositório

- `Contexto/proposta_analisador_funcional_desempenho_escolar.md`: revisão 2 (seção 15), com o exemplo da seção 7 em lambdas e o estilo registrado.
- `GUIA.md` (guia de estudo, fora do git): atualizadas a linha da interface e a data de referência. Ainda há informações antigas (descrição do `teste.py`, `CMD` do Dockerfile, porta do compose e recomendação sobre o pandas).

---

## 4. Controle de versão

| Commit | Conteúdo |
|---|---|
| `2d56105` | Correlação, seleção de disciplina, leitura separada em `dados.py`, `agrupar_por` e `teste.py` |
| `165f04d` | Análises da proposta, validação, resumo geral, erros de arquivo e conversão para expressões |
| `044a5d6` | Testes `unittest`, README, Dockerfile com Streamlit, `tasks.md`, `.gitignore` e lock fora do versionamento |
| (este) | Este relatório atualizado |

- **PR #1:** https://github.com/ArthurAmaral02/analise_escolar/pull/1 (com descrição e comentários atualizados).
- **Não versionados:** `GUIA.md` (fora do git, por escolha) e `.venv/` (ignorado).

---

## 5. Verificação realizada

| Verificação | Resultado |
|---|---|
| Testes automatizados (`unittest`), 81 casos | Todos passam, localmente (Python 3.10) e no container (Python 3.11) |
| Teste de sensibilidade: limite de aprovação trocado de 10 para 9 numa cópia descartável | 5 testes falham, como esperado |
| Pearson e Spearman comparados com `pandas.corr` (G1, G2, G3, studytime, absences, failures, schoolsup) | Iguais, nos dois arquivos |
| Resumo geral comparado com pandas (total, aprovados, percentual, média, mediana) | Iguais, nos dois arquivos |
| Faixas de faltas: soma das contagens | Igual ao total de alunos |
| Validações comparadas com as funções originais do git | Idênticas, nos dois arquivos |
| Erro de arquivo inexistente e de coluna inesperada | Capturados pela interface e pelos testes |
| Estatísticas comparadas com built-ins e `statistics.median` em 2000 listas aleatórias | Iguais |
| Saídas de 39 funções antes e depois da conversão para expressões | Todas iguais |
| Interface Streamlit (`AppTest`): todas as páginas, nas duas disciplinas, com e sem o filtro de zeros | Sem exceções |
| Container Docker: `docker compose up -d --build` | Interface responde em `http://localhost:8080` (HTTP 200) |

**Números de referência:**

| | Matemática | Português |
|---|---|---|
| Registros no arquivo | 395 | 649 |
| `G3 = 0` | 38 | 15 |
| Considerados (sem `G3 = 0`) | 357 | 634 |
| Aprovados (sem `G3 = 0`) | 265 (74,2%) | 549 (86,6%) |
| Correlação G2 × G3 de Pearson (com zeros → sem zeros) | 0,905 → 0,966 | — |

**Ambiente de teste:** Python 3.10 do sistema, com pandas 2.3.3, streamlit 1.65.0 e plotly 7.1.0. O scipy foi usado só para comparação, fora do projeto. O Docker usa Python 3.11.

---

## 6. Pendências

**Análise e documentação**
1. Etapa 8 do `tasks.md`: interpretação escrita dos resultados e conclusões (depende de análise, não de código).
2. Análise de `guardian` como variável de agrupamento (ainda não está entre as variáveis de agrupamento).
3. Comparação escrita entre dias úteis e fins de semana (`Dalc` e `Walc`).
4. ANOVA e Kruskal-Wallis, previstos no `tasks.md`, não implementados. A proposta cita biblioteca padrão; se forem exigidos, precisam ser implementados à mão.
5. Atualizar as informações antigas do `GUIA.md` (ver seção 3.3), se for necessário.

**Código**
6. Trocar `use_container_width` por `width="stretch"` (aviso de depreciação do Streamlit).
7. Melhorar a mensagem de `KeyError` (hoje mostra só a chave).
8. `app/interface/app.py` ainda usa comandos (`try/except`, `if/elif` para páginas e chamadas `st.*`). O restante é próprio do Streamlit.

**Decisões**
9. Confirmar com a equipe o padrão de `G3 = 0` (excluído por padrão).
10. Decidir sobre `app/src/teste.py`: é um rascunho e pode ser apagado.

---

## 7. Como rodar

```bash
cd analise_escolar
python3 -m venv .venv && source .venv/bin/activate
pip install -r app/requirements.txt
cd app/interface
streamlit run app.py --server.port=8080
```

Com Docker (a porta 8080 precisa estar livre):

```bash
docker compose up -d --build
```

Testes:

```bash
cd app
python -m unittest discover -s tests -v
```
