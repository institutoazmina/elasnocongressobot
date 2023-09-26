import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe

# Load the credentials from the corresponding JSON file
gc = gspread.service_account(filename='../dados/appcivico-teste-6a9ded47ac8d.json')

# Open the Google Spreadsheet (replace 'Your-worksheet-name' with your actual worksheet name)
sh = gc.open('AzMina - Elasnocongresso')

# Select the first sheet in the Spreadsheet
worksheet = sh.get_worksheet(1)

# Load your CSV file into a pandas DataFrame
df = pd.read_csv('senado.csv')

# Clear existing data in the worksheet
worksheet.clear()

# Upload DataFrame to the worksheet
set_with_dataframe(worksheet, df)