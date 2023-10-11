import pandas as pd

df = pd.read_csv('camara.csv')

print("Before renaming:")
print(df.columns)

new_columns = {
    'dataHora': 'dataDaTramitacao',
    'nome': 'autor',
    'tipo': 'cargo'
}

# Rename the column names
df.rename(columns=new_columns, inplace=True)

# Print the new column names
print("\nAfter renaming:")
print(df.columns)

# Save the dataframe back to CSV
df.to_csv('camara.csv', index=False)