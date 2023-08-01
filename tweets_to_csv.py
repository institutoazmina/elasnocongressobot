import pandas as pd
import gspread
import json
import csv
import os
from dotenv import load_dotenv # ler variaveis de ambiente do arquivo .env
from oauth2client.service_account import ServiceAccountCredentials
load_dotenv()


if not os.getenv("GOOGLE_JSON_KEY"):
    print("Faltando configurar ENV CONSUMER_KEY")
    raise
if not os.getenv("SPREADSHEET_NAME"):
    print("Faltando configurar ENV CONSUMER_SECRET")
    raise


# Use the JSON key file you downloaded to authenticate and create an API client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_JSON_KEY"), scope)
client = gspread.authorize(creds)

# Open the Google Spreadsheet (replace 'My test sheet' with your sheet's name)
## TODO change sheet matching the year.
sheet = client.open(os.getenv("SPREADSHEET_NAME")).sheet1

try:
    # Try to read the existing CSV file into a DataFrame
    try:
        existing_df = pd.read_csv('output.csv').fillna('')
    except pd.errors.EmptyDataError:
        # If the CSV file is empty, download the data from the Google Spreadsheet
        data = sheet.get_all_values()
        existing_df = pd.DataFrame(data)
        existing_df.to_csv('output.csv', index=False)
    
    # Read the JSON file
    with open('dados/tweets.json', 'r') as f:
        data = json.load(f)
    
    # Check if data is empty
    if not data:
        print("No data in tweets.json")
    else:
        # Decode the JSON strings into dictionaries
        tweets = [json.loads(item) for item in data]
    
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(tweets)
        df.replace([pd.np.nan, pd.np.inf, -pd.np.inf], '')

        # Check if 'hash' column exists in both dataframes
        if 'hash' in df.columns and 'hash' in existing_df.columns:
            # Remove rows from df that have a hash that exists in existing_df
            df = df[~df['hash'].isin(existing_df['hash'])]
        
        # Convert the DataFrame to CSV data and append it to the existing CSV file
        with open('output.csv', 'a') as f:
            df.to_csv(f, header=f.tell()==0, index=False)
        
        # Read the CSV file
        with open('output.csv', 'r') as f:
            csv_data = f.read()
        
        # Use the csv module to split the lines into cells
        csv_reader = csv.reader(csv_data.splitlines())
        csv_cells = list(csv_reader)

        # Prepend the new rows to the existing data
        updated_df = pd.concat([df, existing_df], ignore_index=True)

        updated_df.replace([pd.np.nan, pd.np.inf, -pd.np.inf], '')

        # Write the updated DataFrame to the CSV file
        updated_df.to_csv('output.csv', index=False)
        
        # Convert the updated DataFrame to a list of lists
        csv_cells = [updated_df.columns.tolist()] + updated_df.values.tolist()

        # Remove the hash column
        csv_cells = [row[:-1] for row in csv_cells]

        # Clear the sheet
        sheet.clear()

        # Append the updated data back to the sheet
        sheet.append_rows(csv_cells)
except ValueError as e:
    print(f"Error while reading JSON: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
