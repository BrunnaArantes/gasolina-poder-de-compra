from pathlib import Path

import pandas as pd


# ============================================================
# CONFIGURAÇÕES DO PROJETO
# ============================================================

# Caminho principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Pastas do projeto
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Garante que a pasta processed exista
PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Arquivos originais
ANP_PATH = RAW_DIR / "anp_gasolina.xlsx"
IPCA_PATH = RAW_DIR / "ipca.csv"
# Arquivo original do salário mínimo
SALARIO_PATH = RAW_DIR / "salario_minimo.csv"

# ============================================================
# ANP
# ============================================================

print("=" * 60)
print("PREPARAÇÃO DOS DADOS DA ANP")
print("=" * 60)

print("\nCarregando dados da ANP...")

anp = pd.read_excel(
    ANP_PATH,
    sheet_name="BRASIL - DESDE JANEIRO DE 2013",
    header=16
)


# ------------------------------------------------------------
# Inspeção inicial
# ------------------------------------------------------------

print("\nColunas carregadas:")
print(anp.columns.tolist())

print("\nDimensão da tabela:")
print(anp.shape)

print("\nPrimeiras 5 linhas:")
print(anp.head().to_string())

print("\nProdutos encontrados:")
print(
    anp["PRODUTO"]
    .dropna()
    .unique()
)


# ------------------------------------------------------------
# Filtra somente gasolina comum
# ------------------------------------------------------------

gasolina = anp[
    anp["PRODUTO"] == "GASOLINA COMUM"
].copy()

print("\nApós filtrar GASOLINA COMUM:")
print(
    f"Quantidade de linhas: "
    f"{len(gasolina)}"
)

print("\nProdutos restantes:")
print(
    gasolina["PRODUTO"]
    .unique()
)


# ------------------------------------------------------------
# Seleciona somente as colunas relevantes
# ------------------------------------------------------------

gasolina = gasolina[
    [
        "MÊS",
        "NÚMERO DE POSTOS PESQUISADOS",
        "PREÇO MÉDIO REVENDA"
    ]
].copy()

print("\nApós selecionar as colunas relevantes:")
print(
    gasolina
    .head()
    .to_string()
)


# ------------------------------------------------------------
# Renomeia as colunas
# ------------------------------------------------------------

gasolina = gasolina.rename(
    columns={
        "MÊS": "data",
        "NÚMERO DE POSTOS PESQUISADOS": "postos_pesquisados",
        "PREÇO MÉDIO REVENDA": "preco_gasolina"
    }
)

print("\nColunas renomeadas:")
print(
    gasolina.columns.tolist()
)


# ------------------------------------------------------------
# Tipos dos dados
# ------------------------------------------------------------

print("\nTipos antes da conversão:")
print(gasolina.dtypes)

gasolina["data"] = pd.to_datetime(
    gasolina["data"],
    errors="coerce"
)

gasolina["preco_gasolina"] = pd.to_numeric(
    gasolina["preco_gasolina"],
    errors="coerce"
)

gasolina["postos_pesquisados"] = pd.to_numeric(
    gasolina["postos_pesquisados"],
    errors="coerce"
)

print("\nTipos após a conversão:")
print(gasolina.dtypes)


# ------------------------------------------------------------
# Valores ausentes
# ------------------------------------------------------------

print("\nValores ausentes:")
print(
    gasolina
    .isna()
    .sum()
)

linhas_com_nulos = gasolina[
    gasolina.isna().any(axis=1)
]

print("\nLinhas com algum valor ausente:")
print(
    linhas_com_nulos
    .to_string()
)


# ------------------------------------------------------------
# Período utilizado no projeto
# ------------------------------------------------------------

gasolina = gasolina[
    gasolina["data"] >= "2015-01-01"
].copy()

# Ordena cronologicamente
gasolina = gasolina.sort_values(
    "data"
)

# Recria o índice
gasolina = gasolina.reset_index(
    drop=True
)


# ------------------------------------------------------------
# Validações da ANP
# ------------------------------------------------------------

print("\nPeríodo após o filtro:")

print("Primeira data:")
print(
    gasolina["data"].min()
)

print("Última data:")
print(
    gasolina["data"].max()
)


print("\nPrimeiras 10 linhas após o filtro:")
print(
    gasolina
    .head(10)
    .to_string()
)

print("\nÚltimas 10 linhas:")
print(
    gasolina
    .tail(10)
    .to_string()
)


print("\nDimensão após o filtro:")
print(gasolina.shape)


# ------------------------------------------------------------
# Duplicidades
# ------------------------------------------------------------

quantidade_duplicadas = (
    gasolina["data"]
    .duplicated()
    .sum()
)

print("\nQuantidade de datas duplicadas:")
print(quantidade_duplicadas)


# ------------------------------------------------------------
# Continuidade mensal
# ------------------------------------------------------------

periodo_completo = pd.date_range(
    start=gasolina["data"].min(),
    end=gasolina["data"].max(),
    freq="MS"
)

meses_faltantes = periodo_completo.difference(
    gasolina["data"]
)

print("\nMeses faltantes:")
print(meses_faltantes)


# ------------------------------------------------------------
# Validação final de nulos
# ------------------------------------------------------------

print("\nValores ausentes após o filtro:")
print(
    gasolina
    .isna()
    .sum()
)


# ------------------------------------------------------------
# Salva a ANP tratada
# ------------------------------------------------------------

ANP_PROCESSED_PATH = (
    PROCESSED_DIR
    / "anp_gasolina_mensal.csv"
)

gasolina.to_csv(
    ANP_PROCESSED_PATH,
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivo da ANP tratado com sucesso!")
print(
    f"Salvo em: "
    f"{ANP_PROCESSED_PATH}"
)


# ============================================================
# IPCA
# ============================================================

print("\n" + "=" * 60)
print("PREPARAÇÃO DOS DADOS DO IPCA")
print("=" * 60)


# ------------------------------------------------------------
# Número-índice
# ------------------------------------------------------------

print(
    "\nCarregando número-índice do IPCA..."
)

ipca_indice = pd.read_csv(
    IPCA_PATH,
    sep=";",
    skiprows=3,
    nrows=1,
    decimal=",",
    encoding="utf-8-sig"
)

print("\nDimensão original do número-índice:")
print(ipca_indice.shape)

print("\nTipos das primeiras colunas:")
print(
    ipca_indice
    .dtypes
    .head()
)


# ------------------------------------------------------------
# Variação mensal
# ------------------------------------------------------------

print(
    "\nCarregando variação mensal do IPCA..."
)

ipca_mensal = pd.read_csv(
    IPCA_PATH,
    sep=";",
    skiprows=10,
    nrows=1,
    decimal=",",
    encoding="utf-8-sig"
)

print("\nDimensão original da variação mensal:")
print(ipca_mensal.shape)

print("\nTipos das primeiras colunas:")
print(
    ipca_mensal
    .dtypes
    .head()
)


# ------------------------------------------------------------
# Unpivot do número-índice
# ------------------------------------------------------------

ipca_indice = ipca_indice.drop(
    columns=["Unnamed: 0"]
)

ipca_indice = ipca_indice.melt(
    var_name="mes",
    value_name="indice_ipca"
)

print("\nNúmero-índice após o unpivot:")
print(
    ipca_indice
    .head(10)
    .to_string(index=False)
)

print("\nDimensão após o unpivot:")
print(ipca_indice.shape)


# ------------------------------------------------------------
# Unpivot da variação mensal
# ------------------------------------------------------------

ipca_mensal = ipca_mensal.drop(
    columns=["Unnamed: 0"]
)

ipca_mensal = ipca_mensal.melt(
    var_name="mes",
    value_name="ipca_mensal"
)

print("\nVariação mensal após o unpivot:")
print(
    ipca_mensal
    .head(10)
    .to_string(index=False)
)

print("\nDimensão após o unpivot:")
print(ipca_mensal.shape)


# ------------------------------------------------------------
# Junta número-índice e variação mensal
# ------------------------------------------------------------

ipca = ipca_indice.merge(
    ipca_mensal,
    on="mes",
    how="inner"
)

print(
    "\nIPCA após juntar "
    "número-índice e variação mensal:"
)

print(
    ipca
    .head(10)
    .to_string(index=False)
)

print("\nDimensão da tabela unificada:")
print(ipca.shape)


# ------------------------------------------------------------
# Conversão dos meses em datas
# ------------------------------------------------------------

meses_pt = {
    "janeiro": "01",
    "fevereiro": "02",
    "março": "03",
    "abril": "04",
    "maio": "05",
    "junho": "06",
    "julho": "07",
    "agosto": "08",
    "setembro": "09",
    "outubro": "10",
    "novembro": "11",
    "dezembro": "12"
}


def converter_mes_para_data(valor):
    nome_mes, ano = valor.split()

    numero_mes = meses_pt[
        nome_mes.lower()
    ]

    return pd.to_datetime(
        f"{ano}-{numero_mes}-01"
    )


ipca["data"] = ipca["mes"].apply(
    converter_mes_para_data
)

print(
    "\nIPCA após converter "
    "os meses em datas:"
)

print(
    ipca
    .head(10)
    .to_string(index=False)
)

print("\nTipos dos dados:")
print(ipca.dtypes)


# ------------------------------------------------------------
# Remove a coluna textual de mês
# ------------------------------------------------------------

ipca = ipca.drop(
    columns=["mes"]
)


# ------------------------------------------------------------
# Organiza as colunas
# ------------------------------------------------------------

ipca = ipca[
    [
        "data",
        "indice_ipca",
        "ipca_mensal"
    ]
]


# ------------------------------------------------------------
# Ordena cronologicamente
# ------------------------------------------------------------

ipca = ipca.sort_values(
    "data"
)

ipca = ipca.reset_index(
    drop=True
)


# ------------------------------------------------------------
# Validação do período do IPCA
# ------------------------------------------------------------

print("\nPeríodo do IPCA:")

print("Primeira data:")
print(
    ipca["data"].min()
)

print("Última data:")
print(
    ipca["data"].max()
)


# ------------------------------------------------------------
# Dimensão final
# ------------------------------------------------------------

print("\nDimensão final do IPCA:")
print(ipca.shape)


# ------------------------------------------------------------
# Duplicidades
# ------------------------------------------------------------

duplicidades_ipca = (
    ipca["data"]
    .duplicated()
    .sum()
)

print(
    "\nQuantidade de datas "
    "duplicadas no IPCA:"
)

print(duplicidades_ipca)


# ------------------------------------------------------------
# Valores ausentes
# ------------------------------------------------------------

print("\nValores ausentes no IPCA:")
print(
    ipca
    .isna()
    .sum()
)


# ------------------------------------------------------------
# Continuidade mensal
# ------------------------------------------------------------

periodo_completo_ipca = pd.date_range(
    start=ipca["data"].min(),
    end=ipca["data"].max(),
    freq="MS"
)

meses_faltantes_ipca = (
    periodo_completo_ipca
    .difference(
        ipca["data"]
    )
)

print("\nMeses faltantes no IPCA:")
print(meses_faltantes_ipca)


# ------------------------------------------------------------
# Visualização final
# ------------------------------------------------------------

print(
    "\nPrimeiras 10 linhas "
    "do IPCA tratado:"
)

print(
    ipca
    .head(10)
    .to_string(index=False)
)

print(
    "\nÚltimas 10 linhas "
    "do IPCA tratado:"
)

print(
    ipca
    .tail(10)
    .to_string(index=False)
)


# ------------------------------------------------------------
# Salva o IPCA tratado
# ------------------------------------------------------------

IPCA_PROCESSED_PATH = (
    PROCESSED_DIR
    / "ipca_mensal.csv"
)

ipca.to_csv(
    IPCA_PROCESSED_PATH,
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nArquivo do IPCA "
    "tratado com sucesso!"
)

print(
    f"Salvo em: "
    f"{IPCA_PROCESSED_PATH}"
)
# ============================================================
# SALÁRIO MÍNIMO
# ============================================================

print("\n" + "=" * 60)
print("PREPARAÇÃO DOS DADOS DO SALÁRIO MÍNIMO")
print("=" * 60)

print("\nCarregando dados do salário mínimo...")

salario = pd.read_csv(
    SALARIO_PATH
)

print("\nDados originais:")
print(
    salario.to_string(index=False)
)

print("\nDimensão original:")
print(salario.shape)

print("\nTipos originais:")
print(salario.dtypes)

salario["vigencia"] = pd.to_datetime(
    salario["vigencia"],
    errors="coerce"
)

salario["salario_minimo"] = pd.to_numeric(
    salario["salario_minimo"],
    errors="coerce"
)

print("\nTipos após a conversão:")
print(salario.dtypes)

print("\nValores ausentes:")
print(
    salario
    .isna()
    .sum()
)

duplicidades_salario = (
    salario["vigencia"]
    .duplicated()
    .sum()
)

print("\nVigências duplicadas:")
print(duplicidades_salario)

salario = salario.sort_values(

    "vigencia"

)

salario = salario.reset_index(

    drop=True

)

calendario_mensal = pd.DataFrame(

    {

        "data": pd.date_range(

            start=ipca["data"].min(),

            end=ipca["data"].max(),

            freq="MS"

        )

    }

)

print("\nCalendário mensal criado:")

print(

    calendario_mensal

    .head(10)

    .to_string(index=False)

)

print("\nQuantidade de meses:")

print(len(calendario_mensal))

salario_mensal = pd.merge_asof(

    calendario_mensal,

    salario,

    left_on="data",

    right_on="vigencia",

    direction="backward"

)

print("\nSalário mínimo expandido mensalmente:")
print(
    salario_mensal
    .head(15)
    .to_string(index=False)
)

print("\nValidação da mudança de 2020:")

print(
    salario_mensal[
        (
            salario_mensal["data"] >= "2020-01-01"
        )
        &
        (
            salario_mensal["data"] <= "2020-04-01"
        )
    ].to_string(index=False)
)

print("\nValidação da mudança de 2023:")

print(
    salario_mensal[
        (
            salario_mensal["data"] >= "2023-03-01"
        )
        &
        (
            salario_mensal["data"] <= "2023-07-01"
        )
    ].to_string(index=False)
)

salario_mensal = salario_mensal.drop(
    columns=["vigencia"]
)

print("\nPeríodo da série mensal do salário mínimo:")

print("Primeira data:")
print(
    salario_mensal["data"].min()
)

print("Última data:")
print(
    salario_mensal["data"].max()
)

print("\nDimensão final:")
print(salario_mensal.shape)

print("\nValores ausentes:")
print(
    salario_mensal
    .isna()
    .sum()
)

duplicidades_salario_mensal = (
    salario_mensal["data"]
    .duplicated()
    .sum()
)

print("\nDatas duplicadas:")
print(duplicidades_salario_mensal)

periodo_completo_salario = pd.date_range(
    start=salario_mensal["data"].min(),
    end=salario_mensal["data"].max(),
    freq="MS"
)

meses_faltantes_salario = (
    periodo_completo_salario
    .difference(
        salario_mensal["data"]
    )
)

print("\nMeses faltantes:")
print(meses_faltantes_salario)

print("\nPrimeiras 10 linhas:")
print(
    salario_mensal
    .head(10)
    .to_string(index=False)
)

print("\nÚltimas 10 linhas:")
print(
    salario_mensal
    .tail(10)
    .to_string(index=False)
)

SALARIO_PROCESSED_PATH = (
    PROCESSED_DIR
    / "salario_minimo_mensal.csv"
)

salario_mensal.to_csv(
    SALARIO_PROCESSED_PATH,
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nArquivo do salário mínimo "
    "tratado com sucesso!"
)

print(
    f"Salvo em: "
    f"{SALARIO_PROCESSED_PATH}"
)

# ============================================================
# BASE ANALÍTICA INTEGRADA
# ============================================================

print("\n" + "=" * 60)
print("INTEGRAÇÃO DAS BASES")
print("=" * 60)


# ------------------------------------------------------------
# Usa o IPCA como calendário principal
# ------------------------------------------------------------

base_analitica = ipca.copy()


# ------------------------------------------------------------
# Junta o salário mínimo
# ------------------------------------------------------------

base_analitica = base_analitica.merge(
    salario_mensal,
    on="data",
    how="left",
    validate="one_to_one"
)

print("\nApós juntar IPCA + salário mínimo:")
print(
    base_analitica
    .head(10)
    .to_string(index=False)
)

print("\nDimensão:")
print(base_analitica.shape)


# ------------------------------------------------------------
# Junta os dados da ANP
# ------------------------------------------------------------

base_analitica = base_analitica.merge(
    gasolina[
        [
            "data",
            "postos_pesquisados",
            "preco_gasolina"
        ]
    ],
    on="data",
    how="left",
    validate="one_to_one"
)


# ------------------------------------------------------------
# Organiza as colunas
# ------------------------------------------------------------

base_analitica = base_analitica[
    [
        "data",
        "preco_gasolina",
        "postos_pesquisados",
        "indice_ipca",
        "ipca_mensal",
        "salario_minimo"
    ]
]


# ------------------------------------------------------------
# Visualização inicial
# ------------------------------------------------------------

print("\nPrimeiras 10 linhas da base integrada:")
print(
    base_analitica
    .head(10)
    .to_string(index=False)
)

print("\nÚltimas 10 linhas da base integrada:")
print(
    base_analitica
    .tail(10)
    .to_string(index=False)
)


# ------------------------------------------------------------
# Dimensão
# ------------------------------------------------------------

print("\nDimensão da base integrada:")
print(base_analitica.shape)


# ------------------------------------------------------------
# Duplicidades
# ------------------------------------------------------------

duplicidades_base = (
    base_analitica["data"]
    .duplicated()
    .sum()
)

print("\nDatas duplicadas na base integrada:")
print(duplicidades_base)


# ------------------------------------------------------------
# Valores ausentes
# ------------------------------------------------------------

print("\nValores ausentes na base integrada:")
print(
    base_analitica
    .isna()
    .sum()
)

linhas_incompletas = base_analitica[
    base_analitica.isna().any(axis=1)
]

print("\nLinhas com algum valor ausente:")
print(
    linhas_incompletas
    .to_string(index=False)
)


# ------------------------------------------------------------
# Validação específica de setembro de 2020
# ------------------------------------------------------------

print("\nValidação de setembro de 2020:")

print(
    base_analitica[
        base_analitica["data"] == "2020-09-01"
    ].to_string(index=False)
)


# ------------------------------------------------------------
# Continuidade mensal
# ------------------------------------------------------------

periodo_completo_base = pd.date_range(
    start=base_analitica["data"].min(),
    end=base_analitica["data"].max(),
    freq="MS"
)

meses_faltantes_base = (
    periodo_completo_base
    .difference(
        base_analitica["data"]
    )
)

print("\nMeses ausentes da base integrada:")
print(meses_faltantes_base)


# ------------------------------------------------------------
# Período
# ------------------------------------------------------------

print("\nPeríodo da base integrada:")

print("Primeira data:")
print(
    base_analitica["data"].min()
)

print("Última data:")
print(
    base_analitica["data"].max()
)


# ------------------------------------------------------------
# Salva a base integrada
# ------------------------------------------------------------

BASE_ANALITICA_PATH = (
    PROCESSED_DIR
    / "base_analitica.csv"
)

base_analitica.to_csv(
    BASE_ANALITICA_PATH,
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nBase analítica integrada "
    "salva com sucesso!"
)

print(
    f"Salvo em: "
    f"{BASE_ANALITICA_PATH}"
)

# ============================================================
# MÉTRICAS ANALÍTICAS
# ============================================================

print("\n" + "=" * 60)
print("CRIAÇÃO DAS MÉTRICAS ANALÍTICAS")
print("=" * 60)

# Preserva a base integrada original
base_final = base_analitica.copy()


# ------------------------------------------------------------
# Poder de compra em litros
# ------------------------------------------------------------

base_final["litros_por_salario"] = (
    base_final["salario_minimo"]
    / base_final["preco_gasolina"]
)


# ------------------------------------------------------------
# Custo de um tanque de 50 litros
# ------------------------------------------------------------

base_final["custo_tanque_50l"] = (
    base_final["preco_gasolina"] * 50
)


# ------------------------------------------------------------
# Percentual do salário comprometido por um tanque de 50 L
# ------------------------------------------------------------

base_final["percentual_salario_tanque"] = (
    base_final["custo_tanque_50l"]
    / base_final["salario_minimo"]
    * 100
)


# ------------------------------------------------------------
# Valores-base de janeiro de 2015
# ------------------------------------------------------------

linha_base = base_final[
    base_final["data"] == "2015-01-01"
].iloc[0]

preco_gasolina_base = (
    linha_base["preco_gasolina"]
)

indice_ipca_base = (
    linha_base["indice_ipca"]
)

salario_base = (
    linha_base["salario_minimo"]
)


# ------------------------------------------------------------
# Índices base 100
# ------------------------------------------------------------

base_final["indice_gasolina_100"] = (
    base_final["preco_gasolina"]
    / preco_gasolina_base
    * 100
)

base_final["indice_ipca_100"] = (
    base_final["indice_ipca"]
    / indice_ipca_base
    * 100
)

base_final["indice_salario_100"] = (
    base_final["salario_minimo"]
    / salario_base
    * 100
)


# ------------------------------------------------------------
# Preço da gasolina corrigido pela inflação
# Valores expressos em reais do último mês disponível
# ------------------------------------------------------------

indice_ipca_referencia = (
    base_final.loc[
        (
            base_final["data"]
            == base_final["data"].max()
        ),
        "indice_ipca"
    ]
    .iloc[0]
)

base_final["preco_gasolina_real"] = (
    base_final["preco_gasolina"]
    * (
        indice_ipca_referencia
        / base_final["indice_ipca"]
    )
)


# ------------------------------------------------------------
# Organização das colunas
# ------------------------------------------------------------

base_final = base_final[
    [
        "data",
        "preco_gasolina",
        "preco_gasolina_real",
        "postos_pesquisados",
        "indice_ipca",
        "ipca_mensal",
        "salario_minimo",
        "litros_por_salario",
        "custo_tanque_50l",
        "percentual_salario_tanque",
        "indice_gasolina_100",
        "indice_ipca_100",
        "indice_salario_100"
    ]
]


# ------------------------------------------------------------
# Visualização
# ------------------------------------------------------------

print("\nPrimeiras 10 linhas com métricas:")
print(
    base_final
    .head(10)
    .to_string(index=False)
)

print("\nÚltimas 10 linhas com métricas:")
print(
    base_final
    .tail(10)
    .to_string(index=False)
)


# ------------------------------------------------------------
# Validação da data-base
# ------------------------------------------------------------

print(
    "\nValidação da data-base "
    "- janeiro de 2015:"
)

print(
    base_final[
        base_final["data"] == "2015-01-01"
    ].to_string(index=False)
)


# ------------------------------------------------------------
# Validação da ausência da ANP em setembro/2020
# ------------------------------------------------------------

print("\nValidação de setembro de 2020:")

print(
    base_final[
        base_final["data"] == "2020-09-01"
    ].to_string(index=False)
)


# ------------------------------------------------------------
# Validação do último período
# ------------------------------------------------------------

print("\nValidação do último período:")

print(
    base_final[
        (
            base_final["data"]
            == base_final["data"].max()
        )
    ].to_string(index=False)
)


# ------------------------------------------------------------
# Validações finais
# ------------------------------------------------------------

print("\nDimensão da base final:")
print(base_final.shape)

duplicidades_final = (
    base_final["data"]
    .duplicated()
    .sum()
)

print("\nDatas duplicadas:")
print(duplicidades_final)

print("\nValores ausentes na base final:")
print(
    base_final
    .isna()
    .sum()
)


# ------------------------------------------------------------
# Salva a base final
# ------------------------------------------------------------

BASE_FINAL_PATH = (
    PROCESSED_DIR
    / "base_analitica_final.csv"
)

base_final.to_csv(
    BASE_FINAL_PATH,
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nBase analítica final "
    "salva com sucesso!"
)

print(
    f"Salvo em: "
    f"{BASE_FINAL_PATH}"
)

# ============================================================
# VALIDAÇÃO ANALÍTICA
# ============================================================

print("\n" + "=" * 60)
print("VALIDAÇÃO ANALÍTICA DAS MÉTRICAS")
print("=" * 60)


# ------------------------------------------------------------
# Primeiro e último período disponíveis
# ------------------------------------------------------------

inicio = base_final.iloc[0]
fim = base_final.iloc[-1]


# ------------------------------------------------------------
# Variações percentuais
# ------------------------------------------------------------

variacao_gasolina = (
    fim["preco_gasolina"]
    / inicio["preco_gasolina"]
    - 1
) * 100

variacao_ipca = (
    fim["indice_ipca"]
    / inicio["indice_ipca"]
    - 1
) * 100

variacao_salario = (
    fim["salario_minimo"]
    / inicio["salario_minimo"]
    - 1
) * 100

variacao_litros = (
    fim["litros_por_salario"]
    / inicio["litros_por_salario"]
    - 1
) * 100

variacao_custo_tanque = (
    fim["custo_tanque_50l"]
    / inicio["custo_tanque_50l"]
    - 1
) * 100

variacao_percentual_tanque = (
    fim["percentual_salario_tanque"]
    - inicio["percentual_salario_tanque"]
)


# ------------------------------------------------------------
# Gasolina em termos reais
# ------------------------------------------------------------

variacao_real_gasolina = (
    fim["preco_gasolina_real"]
    / inicio["preco_gasolina_real"]
    - 1
) * 100


# ------------------------------------------------------------
# Diferenças entre os índices
# ------------------------------------------------------------

gasolina_acima_ipca = (
    variacao_gasolina
    - variacao_ipca
)

gasolina_acima_salario = (
    variacao_gasolina
    - variacao_salario
)

salario_acima_ipca = (
    variacao_salario
    - variacao_ipca
)


# ------------------------------------------------------------
# Exibição do resumo
# ------------------------------------------------------------

print("\nPeríodo analisado:")
print(
    f"{inicio['data'].date()} "
    f"até "
    f"{fim['data'].date()}"
)

print("\nVariação do preço da gasolina:")
print(
    f"{variacao_gasolina:.2f}%"
)

print("\nVariação acumulada do IPCA:")
print(
    f"{variacao_ipca:.2f}%"
)

print("\nVariação do salário mínimo:")
print(
    f"{variacao_salario:.2f}%"
)

print("\nVariação dos litros compráveis por um salário mínimo:")
print(
    f"{variacao_litros:.2f}%"
)

print("\nVariação do custo de um tanque de 50 L:")
print(
    f"{variacao_custo_tanque:.2f}%"
)

print(
    "\nMudança no percentual do salário "
    "necessário para um tanque de 50 L:"
)
print(
    f"{variacao_percentual_tanque:.2f} "
    "pontos percentuais"
)

print("\nVariação real da gasolina, descontada a inflação:")
print(
    f"{variacao_real_gasolina:.2f}%"
)

print(
    "\nDiferença entre crescimento da gasolina "
    "e inflação:"
)
print(
    f"{gasolina_acima_ipca:.2f} "
    "pontos percentuais"
)

print(
    "\nDiferença entre crescimento da gasolina "
    "e salário mínimo:"
)
print(
    f"{gasolina_acima_salario:.2f} "
    "pontos percentuais"
)

print(
    "\nDiferença entre crescimento do salário mínimo "
    "e inflação:"
)
print(
    f"{salario_acima_ipca:.2f} "
    "pontos percentuais"
)