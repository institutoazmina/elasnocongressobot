import pandas as pd
import gspread
import json
import csv
from oauth2client.service_account import ServiceAccountCredentials

# Use the JSON key file you downloaded to authenticate and create an API client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('dados/appcivico-teste-6a9ded47ac8d.json', scope)
client = gspread.authorize(creds)

# Open the Google Spreadsheet (replace 'My test sheet' with your sheet's name)
sheet = client.open('Teste').sheet1

try:
    # Try to read the existing CSV file into a DataFrame
    try:
        existing_df = pd.read_csv('output.csv')
    except pd.errors.EmptyDataError:
        # If the CSV file is empty, download the data from the Google Spreadsheet
        data = sheet.get_all_values()
        existing_df = pd.DataFrame(data)
        existing_df.to_csv('output.csv', index=False)
    
    # Read the JSON file
    with open('dados/tweets.json', 'r') as f:
        data = json.load(f)
    
    # Decode the JSON strings into dictionaries
    tweets = [json.loads(item) for item in data]
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(tweets)
    
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
    
    # Remove the hash column
    csv_cells = [row[:-1] for row in csv_cells]
    
    # Clear all existing data in the sheet and upload new data
    sheet.append_rows(csv_cells)
except ValueError as e:
    print(f"Error while reading JSON: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")