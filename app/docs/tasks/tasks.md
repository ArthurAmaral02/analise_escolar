
# Plano de Análise de Correlação — Student Performance

## 1. Objetivo

Investigar quais fatores estão associados ao desempenho escolar dos alunos, utilizando o dataset Student Performance.

A análise será dividida em grupos de variáveis para identificar possíveis relações entre:
- Notas das avaliações;
- Hábitos de estudo;
- Contexto familiar;
- Comportamento e saúde;
- Condições pessoais e sociais.

**Importante:** correlação indica associação entre variáveis, mas não comprova causalidade.

---

# 2. Planejamento das análises

## 2.1. Relação entre G1, G2 e G3

**Objetivo:** investigar a relação entre as notas das três avaliações.

Comparações:
- G1 × G2
- G1 × G3
- G2 × G3

Gráficos recomendados:
- Matriz de correlação;
- Gráficos de dispersão (Scatter Plot).

Perguntas:
- O desempenho na primeira avaliação está relacionado ao desempenho final?
- Existe uma relação forte entre G2 e G3?
- O desempenho dos alunos permanece consistente ao longo das avaliações?

Observação: G1 e G2 fazem parte do processo de avaliação que resulta em G3. Portanto, correlações elevadas são esperadas.

## 2.2. Hábitos de estudo e desempenho

**Objetivo:** investigar como os hábitos dos alunos estão associados às notas finais.

Variáveis:
- `studytime`: tempo semanal de estudo;
- `absences`: quantidade de faltas;
- `failures`: reprovações anteriores;
- `freetime`: tempo livre;
- `goout`: frequência de saídas com amigos.

Comparações:
- studytime × G3
- absences × G3
- failures × G3
- freetime × G3
- goout × G3

Gráficos recomendados:
- Matriz de correlação;
- Scatter Plot;
- Box Plot.

Perguntas:
- Alunos que estudam mais apresentam notas maiores?
- O número de faltas está associado a notas menores?
- Reprovações anteriores estão relacionadas a um desempenho inferior?
- Existe relação entre tempo livre e desempenho?

## 2.3. Contexto familiar e desempenho

**Objetivo:** investigar a relação entre características familiares e desempenho escolar.

Variáveis:
- `Medu`: escolaridade da mãe;
- `Fedu`: escolaridade do pai;
- `famsup`: apoio educacional familiar;
- `famrel`: qualidade das relações familiares;
- `guardian`: responsável pelo aluno.

Comparações:
- Medu × G3
- Fedu × G3
- famsup × G3
- famrel × G3
- guardian × G3

Gráficos recomendados:
- Box Plot;
- Gráficos de barras com médias;
- Matriz de correlação para variáveis ordinais.

Perguntas:
- A escolaridade dos pais está associada às notas?
- O apoio familiar apresenta relação com o desempenho?
- Existe diferença entre os grupos conforme o responsável pelo aluno?

## 2.4. Consumo de álcool e desempenho

**Objetivo:** investigar possíveis associações entre consumo de álcool e desempenho escolar.

Variáveis:
- `Dalc`: consumo de álcool durante a semana;
- `Walc`: consumo de álcool nos finais de semana.

Comparações:
- Dalc × G3
- Walc × G3

Gráficos recomendados:
- Box Plot;
- Gráficos de barras com médias;
- Correlação de Spearman.

Perguntas:
- O consumo durante a semana está associado às notas?
- O consumo nos finais de semana apresenta uma associação diferente?
- Existe alguma tendência entre os níveis de consumo e o desempenho?

## 2.5. Condições pessoais e sociais

**Objetivo:** investigar outras características que podem apresentar associação com o desempenho.

Variáveis:
- `age`: idade;
- `health`: estado de saúde;
- `goout`: frequência de saídas;
- `romantic`: relacionamento amoroso;
- `internet`: acesso à internet;
- `schoolsup`: apoio escolar.

Comparações:
- age × G3
- health × G3
- goout × G3
- romantic × G3
- internet × G3
- schoolsup × G3

Gráficos recomendados:
- Box Plot;
- Scatter Plot;
- Gráficos de barras com médias.

---

# 3. Métodos estatísticos

A escolha do método deve considerar o tipo de variável.

| Tipo de variável | Método recomendado |
|---|---|
| Numéricas | Pearson ou Spearman |
| Ordinais | Spearman |
| Binárias | Correlação ponto-bisserial ou comparação entre grupos |
| Nominais | ANOVA ou Kruskal-Wallis |

### Correlação de Pearson

Indicada para investigar relações lineares entre variáveis numéricas.

### Correlação de Spearman

Indicada para investigar relações monotônicas, especialmente com variáveis ordinais.

### Comparação entre grupos

Para variáveis categóricas, podemos comparar a distribuição das notas entre os grupos.

**Recomendação:** utilizar Spearman como método inicial para investigar as relações entre variáveis ordinais e notas.

---

# 4. Organização da interface

Criar uma nova página no menu lateral:

**Análise de correlação**

A página será dividida em três áreas principais:

### 4.1. Matriz de correlação

- Heatmap com os coeficientes de correlação;
- Identificação de correlações positivas e negativas;
- Exibição dos valores dos coeficientes;
- Possibilidade de separar as variáveis por grupos.

### 4.2. Análise individual

- Seleção de duas variáveis;
- Gráfico de dispersão;
- Linha de tendência quando apropriado;
- Exibição do coeficiente de correlação.

### 4.3. Comparação por categorias

- Seleção de uma variável categórica;
- Comparação das notas G3 entre os grupos;
- Box Plot;
- Média e quantidade de alunos por grupo.

---

# 5. Checklist de desenvolvimento

A ordem abaixo considera dependências entre as etapas e prioriza a construção de uma análise estatística consistente.

## Etapa 1 — Preparação dos dados

- [ ] Revisar as variáveis disponíveis no dataset.
- [ ] Separar variáveis numéricas, ordinais, binárias e nominais.
- [ ] Verificar se todas as variáveis estão corretamente codificadas.
- [ ] Conferir valores ausentes e possíveis inconsistências.
- [ ] Separar G1, G2 e G3 para análises específicas.

## Etapa 2 — Análise das avaliações

- [ ] Calcular a correlação G1 × G2.
- [ ] Calcular a correlação G1 × G3.
- [ ] Calcular a correlação G2 × G3.
- [ ] Criar gráficos de dispersão.
- [ ] Criar matriz de correlação das avaliações.
- [ ] Interpretar os resultados.

## Etapa 3 — Hábitos de estudo

- [ ] Analisar studytime × G3.
- [ ] Analisar absences × G3.
- [ ] Analisar failures × G3.
- [ ] Analisar freetime × G3.
- [ ] Analisar goout × G3.
- [ ] Criar gráficos para as comparações.
- [ ] Interpretar os resultados.

## Etapa 4 — Contexto familiar

- [ ] Analisar Medu × G3.
- [ ] Analisar Fedu × G3.
- [ ] Analisar famsup × G3.
- [ ] Analisar famrel × G3.
- [ ] Analisar guardian × G3.
- [ ] Complementar a análise das profissões dos pais.
- [ ] Criar gráficos comparativos.
- [ ] Interpretar os resultados.

## Etapa 5 — Consumo de álcool e desempenho

- [ ] Analisar Dalc × G3.
- [ ] Analisar Walc × G3.
- [ ] Comparar os resultados dos dias de semana e finais de semana.
- [ ] Criar Box Plots.
- [ ] Interpretar os resultados.

## Etapa 6 — Condições pessoais e sociais

- [ ] Analisar age × G3.
- [ ] Analisar health × G3.
- [ ] Analisar goout × G3.
- [ ] Analisar romantic × G3.
- [ ] Analisar internet × G3.
- [ ] Analisar schoolsup × G3.
- [ ] Criar gráficos comparativos.
- [ ] Interpretar os resultados.

## Etapa 7 — Desenvolvimento da interface

- [ ] Criar a página "Análise de correlação".
- [ ] Implementar a matriz de correlação.
- [ ] Implementar o Heatmap.
- [ ] Implementar seleção de variáveis.
- [ ] Implementar gráficos de dispersão.
- [ ] Implementar linha de tendência.
- [ ] Implementar comparação por categorias.
- [ ] Adicionar indicadores estatísticos.
- [ ] Organizar os gráficos e descrições na interface.

## Etapa 8 — Interpretação e conclusão

- [ ] Identificar as correlações mais relevantes.
- [ ] Identificar relações positivas e negativas.
- [ ] Identificar variáveis com pouca ou nenhuma associação.
- [ ] Comparar os resultados entre os diferentes grupos.
- [ ] Verificar a quantidade de alunos em cada grupo.
- [ ] Evitar interpretações causais sem evidências.
- [ ] Elaborar conclusões com base nos resultados encontrados.

---

# 6. Ordem de prioridade

| Prioridade | Análise |
|---|---|
| 1 | Correlação entre G1, G2 e G3 |
| 2 | Hábitos de estudo |
| 3 | Contexto familiar |
| 4 | Consumo de álcool |
| 5 | Condições pessoais e sociais |
| 6 | Interface interativa |
| 7 | Interpretação e conclusão |

---

# 7. Resultado esperado do projeto

Ao finalizar essas etapas, o sistema deverá permitir:

1. Visualizar as relações entre as variáveis do dataset.
2. Identificar fatores associados ao desempenho escolar.
3. Comparar grupos de alunos.
4. Investigar relações positivas, negativas ou fracas.
5. Visualizar os resultados por meio de gráficos interativos.
6. Produzir conclusões fundamentadas nos dados.

**Objetivo final:** transformar o dataset Student Performance em uma ferramenta exploratória de análise do desempenho escolar, permitindo investigar padrões e associações entre características dos alunos e suas notas.
