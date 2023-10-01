import gspread
s=gspread.service_account(filename="%APPDATA%\gspread\service_account.json")
sa=s.open("annual-enterprise-survey-2021-financial-year-provisional-csv")
x=sa.worksheet("annual-enterprise-survey-2021-financial-year-provisional-csv")
print(x.row_count)
