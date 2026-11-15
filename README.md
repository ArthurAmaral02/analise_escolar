comando para rodar o "site"

tem que dar esse comando no diretorio interface

streamlit run app.py --server.address=0.0.0.0 --server.port=8080

## Decisões de análise

- **Interface:** Streamlit (página de terminal descartada). A proposta original previa só terminal; essa mudança precisa ser comunicada à professora.
- **Aprovação:** `G3 >= 10` é aprovado; `G3 < 10` é reprovado. É uma regra analítica do projeto, não a regra oficial da escola.
- **G3 = 0:** excluído das análises por padrão (checkbox na barra lateral). Em Matemática, 25 dos 38 alunos com G3 = 0 tinham G2 > 0, o que sugere abandono ou não conclusão, não nota baixa. Para incluí-los, desmarque a opção.
- **Análises descritivas:** diferenças entre grupos e correlações não comprovam causa e efeito.
