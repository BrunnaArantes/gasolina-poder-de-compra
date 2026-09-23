# Progresso do projeto — Gasolina x Inflação x Salário Mínimo

## ETAPA 1 — Estrutura inicial do projeto

- [x] Criar pasta `gasolina-poder-de-compra`
- [x] Criar pasta `.venv`
- [x] Criar pasta `data/raw`
- [x] Criar pasta `data/processed`
- [x] Criar pasta `src`
- [x] Criar pasta `powerbi`
- [x] Criar pasta `images`
- [x] Criar `README.md`
- [x] Criar `.gitignore`
- [x] Criar `requirements.txt`
- [x] Criar `PROGRESSO.md`

---

## ETAPA 2 — Dados da ANP

- [x] Baixar série histórica mensal oficial da ANP
- [x] Salvar como `data/raw/anp_gasolina.xlsx`
- [x] Preservar arquivo original sem alterações manuais

---

## ETAPA 3 — Dados do IPCA

- [x] Baixar série histórica oficial do IPCA no SIDRA/IBGE
- [x] Utilizar Tabela 1737
- [x] Selecionar número-índice
- [x] Selecionar variação mensal
- [x] Período iniciado em janeiro/2015
- [x] Salvar como `data/raw/ipca.csv`
- [x] Preservar arquivo original sem alterações manuais

---

## ETAPA 4 — Salário mínimo

- [x] Criar `data/raw/salario_minimo.csv`
- [x] Inserir valores históricos de 2015 a 2026
- [x] Considerar mudança de salário em fevereiro/2020
- [x] Considerar mudança de salário em maio/2023
- [x] Usar datas no padrão `YYYY-MM-DD`

---

## ETAPA 5 — Ambiente Python

- [x] Verificar instalação do Python
- [x] Instalar extensão Python no VS Code
- [x] Criar ambiente virtual `.venv`
- [x] Ativar `.venv`
- [x] Atualizar `pip`
- [x] Instalar `pandas`
- [x] Instalar `openpyxl`
- [x] Gerar `requirements.txt`
- [x] Corrigir encoding do `requirements.txt`
- [x] Selecionar interpretador da `.venv`
- [x] Testar execução de Python no projeto

---

## ETAPA 6 — Data Profiling / inspeção inicial

- [x] Criar `src/inspect_data.py`
- [x] Confirmar existência dos três arquivos brutos
- [x] Inspecionar estrutura do salário mínimo
- [x] Verificar tipos do salário mínimo
- [x] Verificar valores ausentes do salário mínimo
- [x] Inspecionar estrutura bruta do IPCA
- [x] Identificar bloco de número-índice
- [x] Identificar bloco de variação mensal
- [x] Identificar separador `;`
- [x] Identificar vírgula como separador decimal original
- [x] Identificar período do IPCA até julho/2026
- [x] Inspecionar abas da ANP
- [x] Identificar aba `BRASIL - DESDE JANEIRO DE 2013`
- [x] Identificar cabeçalho real da ANP na linha 16
- [x] Identificar produto `GASOLINA COMUM`
- [x] Identificar coluna `PREÇO MÉDIO REVENDA`

---

## ETAPA 7 — Tratamento da ANP

- [x] Criar tratamento no `prepare_data.py`
- [x] Ler Excel usando `header=16`
- [x] Filtrar `GASOLINA COMUM`
- [x] Selecionar colunas relevantes
- [x] Manter `MÊS`
- [x] Manter `NÚMERO DE POSTOS PESQUISADOS`
- [x] Manter `PREÇO MÉDIO REVENDA`
- [x] Renomear para `data`
- [x] Renomear para `postos_pesquisados`
- [x] Renomear para `preco_gasolina`
- [x] Validar tipos
- [x] Validar valores ausentes
- [x] Filtrar período a partir de janeiro/2015
- [x] Ordenar cronologicamente
- [x] Validar duplicidades
- [x] Identificar ausência de setembro/2020
- [x] Manter setembro/2020 como ausência real de coleta
- [x] Preservar agosto/2026 existente na ANP
- [x] Gerar `data/processed/anp_gasolina_mensal.csv`

---

## ETAPA 8 — Tratamento do IPCA

- [x] Ler bloco de número-índice
- [x] Ler bloco de variação mensal
- [x] Interpretar decimal brasileiro corretamente
- [x] Confirmar estrutura `(1, 140)` nos dois blocos
- [x] Remover coluna de localidade
- [x] Fazer unpivot do número-índice
- [x] Fazer unpivot da variação mensal
- [x] Transformar estrutura wide → long
- [x] Juntar número-índice e variação mensal
- [x] Converter nomes de meses em datas
- [x] Ordenar cronologicamente
- [x] Validar período janeiro/2015 → julho/2026
- [x] Confirmar 139 meses
- [x] Confirmar zero duplicidades
- [x] Confirmar zero valores ausentes
- [x] Confirmar zero meses faltantes
- [x] Gerar `data/processed/ipca_mensal.csv`

---

## ETAPA 9 — Tratamento do salário mínimo

- [x] Ler `salario_minimo.csv`
- [x] Converter `vigencia` para data
- [x] Converter `salario_minimo` para número
- [x] Validar ausência de nulos
- [x] Validar ausência de vigências duplicadas
- [x] Criar calendário mensal
- [x] Expandir vigências usando `merge_asof`
- [x] Validar mudança de janeiro → fevereiro/2020
- [x] Validar mudança de janeiro → maio/2023
- [x] Gerar série mensal de janeiro/2015 a julho/2026
- [x] Confirmar 139 meses
- [x] Confirmar zero duplicidades
- [x] Confirmar zero nulos
- [x] Confirmar zero meses faltantes
- [x] Gerar `data/processed/salario_minimo_mensal.csv`

---

## ETAPA 10 — Integração das bases

- [x] Usar IPCA como calendário principal
- [x] Integrar salário mínimo
- [x] Integrar ANP
- [x] Usar relacionamento `left` para preservar setembro/2020
- [x] Manter setembro/2020 na base
- [x] Manter gasolina e postos como `NaN` em setembro/2020
- [x] Confirmar 139 linhas
- [x] Confirmar 6 colunas
- [x] Confirmar zero datas duplicadas
- [x] Confirmar continuidade temporal
- [x] Confirmar período janeiro/2015 → julho/2026
- [x] Gerar `data/processed/base_analitica.csv`

---

## ETAPA 11 — Métricas analíticas

- [x] Criar `litros_por_salario`
- [x] Criar `custo_tanque_50l`
- [x] Criar `percentual_salario_tanque`
- [x] Criar `indice_gasolina_100`
- [x] Criar `indice_ipca_100`
- [x] Criar `indice_salario_100`
- [x] Criar `preco_gasolina_real`
- [x] Usar janeiro/2015 como base 100
- [x] Usar julho/2026 como referência do preço real
- [x] Validar índices = 100 em janeiro/2015
- [x] Validar ausência de gasolina em setembro/2020
- [x] Validar `preco_gasolina_real = preco_gasolina` em julho/2026
- [x] Confirmar dimensão `(139, 13)`
- [x] Confirmar zero duplicidades
- [x] Gerar `data/processed/base_analitica_final.csv`

---

## ETAPA 12 — Validação analítica

- [x] Calcular variação da gasolina
- [x] Calcular variação acumulada do IPCA
- [x] Calcular variação do salário mínimo
- [x] Calcular variação dos litros compráveis
- [x] Calcular variação do custo de tanque de 50 L
- [x] Calcular mudança no percentual do salário comprometido
- [x] Calcular variação real da gasolina
- [x] Comparar gasolina x IPCA
- [x] Comparar gasolina x salário mínimo
- [x] Comparar salário mínimo x IPCA
- [x] Validar período janeiro/2015 → julho/2026

### Resultados validados

- [x] Gasolina: +116,69%
- [x] IPCA: +86,31%
- [x] Salário mínimo: +105,71%
- [x] Litros por salário: -5,07%
- [x] Tanque de 50 L: +116,69%
- [x] Comprometimento do salário: +1,03 p.p.
- [x] Alta real da gasolina: +16,31%

---

# ETAPA 13 — Power BI: importação e modelo

## 13.1 — Importação

- [x] Importar `base_analitica_final.csv`
- [x] Abrir no Power Query
- [x] Identificar problema de localidade nos números
- [x] Remover conversão automática incorreta
- [x] Criar transformação com localidade `en-US`
- [x] Validar `preco_gasolina = 3,032` em janeiro/2015
- [x] Validar `preco_gasolina_real ≈ 5,648931`
- [x] Validar `indice_ipca = 4110,2`
- [x] Validar `ipca_mensal = 1,24`
- [x] Validar `postos_pesquisados = 34414`
- [x] Validar `salario_minimo = 788`
- [x] Transformar `postos_pesquisados` em número inteiro
- [x] Confirmar `salario_minimo` como número inteiro
- [x] Confirmar todas as demais métricas como número decimal
- [x] Conferir as 13 colunas no Power Query
- [x] Clicar em `Fechar e Aplicar`

## 13.2 — DimData

- [x] Criar tabela `DimData`
- [x] Criar coluna `Date`
- [x] Criar coluna `Ano`
- [x] Criar coluna `MesNumero`
- [x] Criar coluna `Mes`
- [x] Criar coluna `MesAbreviado`
- [x] Criar coluna `AnoMes`
- [x] Criar coluna `AnoMesNumero`
- [x] Criar coluna `InicioMes`
- [x] Ordenar `Mes` por `MesNumero`
- [x] Ordenar `MesAbreviado` por `MesNumero`
- [x] Ordenar `AnoMes` por `AnoMesNumero`
- [x] Marcar `DimData` como tabela de datas

## 13.3 — Relacionamento

- [x] Relacionar `DimData[Date]` com `base_analitica_final[data]`
- [x] Confirmar cardinalidade `1:*`
- [x] Confirmar `1` do lado de `DimData`
- [x] Confirmar `*` do lado de `base_analitica_final`
- [x] Confirmar direção de filtro `Única`
- [x] Confirmar relacionamento ativo

## 13.4 — Arquivo Power BI

- [x] Salvar em `powerbi/gasolina_poder_de_compra.pbix`

---

# ETAPA 14 — Medidas DAX

- [x] Criar medidas dos KPIs
- [x] Criar medida de preço atual da gasolina
- [x] Criar medida de salário mínimo atual
- [x] Criar medida de litros por salário
- [x] Criar medida de custo do tanque de 50 L
- [x] Criar medida de percentual do salário comprometido
- [x] Criar medidas de variação
- [x] Validar filtros temporais
- [x] Organizar medidas no modelo

---

# ETAPA 15 — Dashboard Power BI

- [x] Definir layout da página
- [x] Criar título principal
- [x] Criar subtítulo com período analisado
- [x] Criar cards de KPI
- [x] Criar gráfico de índices base 100
- [x] Criar gráfico de litros por salário
- [x] Criar gráfico de gasolina nominal x real
- [x] Criar filtros necessários
- [x] Tratar setembro/2020 visualmente
- [x] Revisar formatação numérica
- [x] Revisar textos e títulos
- [x] Refinar UI/UX do dashboard

---

# ETAPA 16 — Insights e conclusão

- [x] Analisar comportamento da gasolina
- [x] Analisar evolução do salário mínimo
- [x] Analisar evolução do IPCA
- [x] Analisar poder de compra
- [x] Identificar períodos relevantes
- [x] Escrever principais insights
- [x] Responder a pergunta central do projeto
- [x] Registrar limitações metodológicas
- [x] Explicar ausência de setembro/2020
- [x] Explicar que 2026 é parcial até julho

---

# ETAPA 17 — README e documentação

- [x] Finalizar título do projeto
- [x] Escrever objetivo
- [x] Escrever pergunta central
- [x] Documentar perguntas de negócio
- [x] Documentar fontes oficiais
- [x] Documentar tecnologias utilizadas
- [x] Documentar pipeline ETL
- [x] Documentar tratamento da ANP
- [x] Documentar tratamento do IPCA
- [x] Documentar tratamento do salário mínimo
- [x] Documentar métricas
- [x] Documentar metodologia
- [x] Documentar limitações
- [x] Adicionar principais insights
- [x] Adicionar conclusão
- [x] Adicionar instruções de execução
- [x] Adicionar estrutura de pastas

---

# ETAPA 18 — Imagens e apresentação

- [x] Finalizar dashboard
- [x] Exportar imagem principal do dashboard
- [x] Salvar em `images/dashboard.png`
- [x] Adicionar imagem ao README
- [x] Revisar aparência no GitHub

---

# ETAPA 19 — Git e GitHub

- [ ] Inicializar repositório Git
- [ ] Conferir `.gitignore`
- [ ] Garantir que `.venv` não será versionada
- [ ] Revisar arquivos que serão publicados
- [ ] Fazer primeiro commit
- [ ] Criar repositório no GitHub
- [ ] Conectar repositório local ao GitHub
- [ ] Fazer push
- [ ] Conferir README no GitHub
- [ ] Conferir arquivos do projeto
- [ ] Adicionar descrição do repositório
- [ ] Adicionar tópicos/tags relevantes

---

# ETAPA 20 — Portfólio e LinkedIn

- [ ] Criar descrição curta do projeto
- [ ] Preparar publicação do LinkedIn
- [ ] Escolher imagem principal
- [ ] Destacar Python/Pandas
- [ ] Destacar ETL
- [ ] Destacar Power BI
- [ ] Destacar DAX
- [ ] Destacar dados oficiais
- [ ] Apresentar principal descoberta sem exagerar conclusões
- [ ] Adicionar link do GitHub
- [ ] Adicionar projeto à seção de projetos do LinkedIn