import gspread
# from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from linkedinAPI import main_df
import os

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
# print("Type of my_dataframe:", type(result_df))

list_from_main_df = result_df.to_numpy().tolist()
print(list_from_main_df)
print("Type of my_dataframe:", type(list_from_main_df))

try:
    spreadsheet = gc.open_by_key(os.getenv('open_by_key'))
    print(f"Successfully opened: {spreadsheet.title}")
    worksheet = spreadsheet.sheet1
    # worksheet.update('A1', 'Hello World!')
    #inserting a new row from top
    values = list_from_main_df
    worksheet.insert_rows(values, row=2, value_input_option='RAW')
    #delete row
    # worksheet.delete_row(index=2)

    # print(f"First row: {worksheet.row_values(1)}")
    print(f"All data: {worksheet.get_all_values()}")

except Exception as e:
    print(f"Error: {str(e)}")