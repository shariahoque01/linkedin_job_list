import gspread
# from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from linkedinAPI import main_df
import os
import pandas as pd


load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(
    'service_acc_key.json',
    scopes=SCOPES
)

gc = gspread.authorize(credentials)

print(credentials)

result_df = main_df()
row_count = len(result_df)
print(f"::notice::Total rows processed: {row_count}")  # GitHub Actions formatted output
print(f"Total rows: {row_count}") 


# print("Type of my_dataframe:", type(result_df))

list_from_main_df = result_df.to_numpy().tolist()
print(list_from_main_df)

# print("Type of my_dataframe:", type(list_from_main_df))

try:
    spreadsheet = gc.open_by_key(os.getenv('open_by_key'))
    print(f"Successfully opened: {spreadsheet.title}")
    worksheet = spreadsheet.sheet1
    ''' Logic 1 for gsspread:
            inserting a new row from top from api
    '''
    values = list_from_main_df
    # print(values.count())
    worksheet.insert_rows(values, row=2, value_input_option='RAW')
    
    ''' Logic2 for gsspread:
            deleting duplicates based on the unique job_id and keep the latest record
    '''
    df = pd.DataFrame(worksheet.get_all_records())
    # print(df.dtypes)
    df = df.drop_duplicates(subset=['Job ID'], keep='first')
    data = [df.columns.values.tolist()] + df.values.tolist()
    worksheet.clear()
    worksheet.update('A1',data)
    #delete row
    # worksheet.delete_row(index=2)
    print(f"Total jobs count in the sheet: {worksheet.row_count}")

except Exception as e:
    print(f"Error: {str(e)}")