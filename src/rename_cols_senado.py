import pandas as pd

df = pd.read_csv("senado.csv")

print("Before renaming:")
print(df.columns)

new_columns = {
    "DataUltimaAtualizacao": "DataDaTramitacao",
    "DescricaoIdentificacaoMateria": "NomeDoProjeto",
}

# Rename the column names
df.rename(columns=new_columns, inplace=True)

# Print the new column names
print("\nAfter renaming:")
print(df.columns)

# Save the dataframe back to CSV
df.to_csv("senado.csv", index=False)
