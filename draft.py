import gspread
# from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from linkedinAPI import main_df
import pandas as pd
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


try:
    spreadsheet = gc.open_by_key(os.getenv('open_by_key'))
    print(f"Successfully opened: {spreadsheet.title}")
    worksheet = spreadsheet.sheet1
    df = pd.DataFrame(worksheet.get_all_records())
    print(df.dtypes)
    df = df.drop_duplicates(subset=['Job ID'], keep='first')
    data = [df.columns.values.tolist()] + df.values.tolist()
    worksheet.clear()
    worksheet.update('A1',data)
    print(df.shape)
    print(worksheet.row_values(1))
except Exception as e:
    print(f"Error: {str(e)}")