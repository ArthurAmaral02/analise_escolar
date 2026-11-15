
# 📊 Student Performance — Dicionário de Dados

Este documento apresenta a descrição das variáveis presentes nos datasets `student-mat.csv` e `student-por.csv`, utilizados no projeto de análise de desempenho escolar.

As variáveis representam informações demográficas, familiares, acadêmicas, sociais e relacionadas à saúde dos estudantes.

---

## 1. Informações pessoais e demográficas

| Variável | Significado | Descrição |
|---|---|---|
| `school` | Escola | Escola em que o aluno estuda: GP (Gabriel Pereira) ou MS (Mousinho da Silveira). |
| `sex` | Sexo | Sexo do estudante: F (feminino) ou M (masculino). |
| `age` | Idade | Idade do estudante, entre 15 e 22 anos. |
| `address` | Endereço | Local onde mora: U (urbano) ou R (rural). |

---

## 2. Informações familiares

| Variável | Significado | Descrição |
|---|---|---|
| `famsize` | Tamanho da família | LE3: até 3 pessoas; GT3: mais de 3 pessoas. |
| `Pstatus` | Estado dos pais | T: pais moram juntos; A: pais moram separados. |
| `Medu` | Escolaridade da mãe | Nível de escolaridade da mãe, de 0 a 4. |
| `Fedu` | Escolaridade do pai | Nível de escolaridade do pai, de 0 a 4. |
| `Mjob` | Profissão da mãe | Profissão ou ocupação da mãe. |
| `Fjob` | Profissão do pai | Profissão ou ocupação do pai. |
| `guardian` | Responsável | Responsável pelo estudante: mãe, pai ou outro. |
| `famrel` | Relação familiar | Qualidade do relacionamento familiar, de 1 a 5. |
| `famsup` | Apoio familiar | Indica se o estudante recebe apoio educacional da família. |

### Escala de escolaridade (Medu e Fedu)

| Valor | Escolaridade |
|---|---|
| 0 | Nenhuma escolaridade |
| 1 | Ensino primário (4ª série) |
| 2 | 5ª a 9ª série |
| 3 | Ensino secundário |
| 4 | Ensino superior |

---

## 3. Informações escolares e acadêmicas

| Variável | Significado | Descrição |
|---|---|---|
| `reason` | Motivo da escolha | Motivo pelo qual o aluno escolheu aquela escola. |
| `traveltime` | Tempo de deslocamento | Tempo gasto para ir de casa até a escola. |
| `studytime` | Tempo de estudo | Quantidade de horas semanais dedicadas aos estudos. |
| `failures` | Reprovações | Número de reprovações anteriores. |
| `schoolsup` | Apoio escolar | Indica se recebe apoio educacional extra da escola. |
| `paid` | Aulas particulares | Indica se participa de aulas extras pagas na disciplina. |
| `higher` | Ensino superior | Indica se deseja cursar o ensino superior. |
| `nursery` | Educação infantil | Indica se frequentou creche ou educação infantil. |
| `G1` | Primeira avaliação | Nota do primeiro período, de 0 a 20. |
| `G2` | Segunda avaliação | Nota do segundo período, de 0 a 20. |
| `G3` | Nota final | Nota final do estudante, de 0 a 20. |

### Escala de tempo de estudo (studytime)

| Valor | Tempo semanal |
|---|---|
| 1 | Menos de 2 horas |
| 2 | De 2 a 5 horas |
| 3 | De 5 a 10 horas |
| 4 | Mais de 10 horas |

---

## 4. Informações sociais e comportamentais

| Variável | Significado | Descrição |
|---|---|---|
| `activities` | Atividades extracurriculares | Indica se participa de atividades fora do currículo escolar. |
| `internet` | Acesso à internet | Indica se possui acesso à internet em casa. |
| `romantic` | Relacionamento amoroso | Indica se está em um relacionamento amoroso. |
| `freetime` | Tempo livre | Quantidade de tempo livre após a escola, de 1 a 5. |
| `goout` | Saídas com amigos | Frequência com que sai com amigos, de 1 a 5. |

---

## 5. Saúde e hábitos pessoais

| Variável | Significado | Descrição |
|---|---|---|
| `Dalc` | Consumo de álcool durante a semana | Nível de consumo de álcool em dias úteis, de 1 a 5. |
| `Walc` | Consumo de álcool no fim de semana | Nível de consumo de álcool nos finais de semana, de 1 a 5. |
| `health` | Estado de saúde | Percepção do próprio estado de saúde, de 1 a 5. |
| `absences` | Faltas | Quantidade de faltas escolares do estudante. |

### Escala de consumo de álcool (Dalc e Walc)

| Valor | Intensidade |
|---|---|
| 1 | Muito baixo |
| 2 | Baixo |
| 3 | Moderado |
| 4 | Alto |
| 5 | Muito alto |

---

## 6. Classificação geral das variáveis

| Grupo | Variáveis |
|---|---|
| Demográficas | `school`, `sex`, `age`, `address` |
| Familiares | `famsize`, `Pstatus`, `Medu`, `Fedu`, `Mjob`, `Fjob`, `guardian`, `famrel`, `famsup` |
| Acadêmicas | `reason`, `traveltime`, `studytime`, `failures`, `schoolsup`, `paid`, `higher`, `nursery`, `G1`, `G2`, `G3` |
| Sociais | `activities`, `internet`, `romantic`, `freetime`, `goout` |
| Saúde e hábitos | `Dalc`, `Walc`, `health`, `absences` |

---

## 7. Características gerais do dataset

O conjunto de dados possui 33 variáveis:

- **32 Features:** variáveis explicativas que representam características dos estudantes.
- **1 Target principal:** variável `G3`, correspondente à nota final do estudante.

As variáveis `G1` e `G2` também representam notas e podem ser utilizadas como variáveis explicativas na análise ou previsão do desempenho final.

---

## 8. Objetivo do pré-processamento

Antes de realizar as análises estatísticas, os dados passarão por uma etapa de pré-processamento.

Essa etapa tem como objetivos:

1. Identificar e tratar variáveis categóricas.
2. Converter variáveis textuais em representações adequadas para análise.
3. Preservar a natureza ordinal das variáveis que possuem hierarquia.
4. Padronizar os tipos de dados numéricos.
5. Verificar valores ausentes e inconsistências.
6. Preparar os dados para análises estatísticas e possíveis aplicações de Machine Learning.

**Importante:** nem toda variável categórica deve ser convertida diretamente em números sequenciais. Variáveis nominais, como `Mjob` e `Fjob`, não possuem uma ordem natural e podem exigir One-Hot Encoding.
