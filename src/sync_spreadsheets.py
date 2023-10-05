import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
from gspread_dataframe import set_with_dataframe
import os
from dotenv import load_dotenv # ler variaveis de ambiente do arquivo .env
load_dotenv()

# Use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_JSON_KEY"), scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first and second sheet
# Make sure you use the right names here.
sheet_camara = client.open(os.getenv("SPREADSHEET_NAME")).get_worksheet(0)  # 0 refers to first sheet
sheet_senado = client.open(os.getenv("SPREADSHEET_NAME")).get_worksheet(1)  # 1 refers to second sheet

def read_csv(file_name):
    with open(file_name, newline='') as f:
        return list(csv.reader(f))

def write_csv(file_name, rows):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def update_csv(input_file, existing_file):
    input_rows = read_csv(input_file)
    existing_rows = read_csv(existing_file)

    # Assuming the id column is the first one
    input_ids = {row[0] for row in input_rows}

    # Remove duplicates
    unique_existing_rows = [row for row in existing_rows if row[0] not in input_ids]
    
    # Prepend new rows
    final_rows = input_rows + unique_existing_rows

    # Write to existing file
    write_csv(existing_file, final_rows)

def update_sheet(sheet, file_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_name)

    # Clear the sheet
    sheet.clear()

    # Update the sheet with the DataFrame
    set_with_dataframe(sheet, df)

# Generate the current date in YMD format
current_date = datetime.now().strftime('%Y%m%d')

update_csv(f'camara_{current_date}.csv', 'camara.csv')
update_sheet(sheet_camara, 'camara.csv')

update_csv(f'senado_{current_date}.csv', 'senado.csv')
update_sheet(sheet_senado, 'senado.csv')
