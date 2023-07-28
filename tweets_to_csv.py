import pandas as pd
import gspread
import json
import csv
from oauth2client.service_account import ServiceAccountCredentials

# Use the JSON key file you downloaded to authenticate and create an API client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('', scope)
client = gspread.authorize(creds)

# Open the Google Spreadsheet (replace 'My test sheet' with your sheet's name)
sheet = client.open('').sheet1

try:
    # Read the JSON file
    with open('dados/tweets.json', 'r') as f:
        data = json.load(f)
    
    # Decode the JSON strings into dictionaries
    tweets = [json.loads(item) for item in data]
    
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(tweets)
    
    # Convert the DataFrame to CSV data
    csv_data = df.to_csv(index=False)
    
    # Use the csv module to split the lines into cells
    csv_reader = csv.reader(csv_data.splitlines())
    csv_cells = list(csv_reader)
    
    # Clear all existing data in the sheet and upload new data
    sheet.clear()
    sheet.append_rows(csv_cells)
except ValueError as e:
    print(f"Error while reading JSON: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")