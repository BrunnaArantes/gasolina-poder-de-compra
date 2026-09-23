from pathlib import Path

import pandas as pd


# Pasta principal do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminhos dos arquivos brutos
RAW_DIR = BASE_DIR / "data" / "raw"

ANP_PATH = RAW_DIR / "anp_gasolina.xlsx"
IPCA_PATH = RAW_DIR / "ipca.csv"
SALARIO_PATH = RAW_DIR / "salario_minimo.csv"


print("=" * 60)
print("INSPEÇÃO INICIAL DOS ARQUIVOS")
print("=" * 60)

print(f"\nPasta do projeto: {BASE_DIR}")
print(f"Pasta dos dados brutos: {RAW_DIR}")

print("\nARQUIVOS ENCONTRADOS:")

print(f"ANP: {ANP_PATH.exists()}")
print(f"IPCA: {IPCA_PATH.exists()}")
print(f"Salário mínimo: {SALARIO_PATH.exists()}")

print("\n" + "=" * 60)
print("SALÁRIO MÍNIMO")
print("=" * 60)

salario = pd.read_csv(SALARIO_PATH)

print("\nPrimeiras linhas:")
print(salario.head())

print("\nÚltimas linhas:")
print(salario.tail())

print("\nColunas:")
print(salario.columns.tolist())

print("\nFormato da tabela:")
print(salario.shape)

print("\nTipos dos dados:")
print(salario.dtypes)

print("\nResumo técnico:")
salario.info()

print("\nValores ausentes:")
print(salario.isna().sum())

print("\n" + "=" * 60)
print("IPCA - INSPEÇÃO DO ARQUIVO BRUTO")
print("=" * 60)

with open(IPCA_PATH, "r", encoding="utf-8-sig") as arquivo:
    for numero_linha in range(15):
        linha = arquivo.readline()
        print(f"{numero_linha + 1}: {linha.rstrip()}")

        print("\n" + "=" * 60)
print("ANP - ABAS DA PLANILHA")
print("=" * 60)

excel_anp = pd.ExcelFile(ANP_PATH)

print("\nAbas encontradas:")
print(excel_anp.sheet_names)

primeira_aba = excel_anp.sheet_names[0]

print(f"\nPrimeira aba selecionada para inspeção: {primeira_aba}")

anp_bruto = pd.read_excel(
    ANP_PATH,
    sheet_name=primeira_aba,
    header=None,
    nrows=30
)

print("\nPrimeiras 30 linhas brutas:")
print(anp_bruto.to_string())