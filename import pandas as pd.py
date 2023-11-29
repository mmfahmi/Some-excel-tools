import pandas as pd

# Load CSV file into a DataFrame
csv_file_path = 'G:/aggregated_data.csv'
df_csv = pd.read_csv(csv_file_path)

# Load Excel file into a DataFrame
excel_file_path = 'G:/email100Excel.xlsx'
df_excel = pd.read_excel(excel_file_path)

# Extract emails from both DataFrames
emails_csv = set(df_csv['email'])
emails_excel = set(df_excel['email'])

# Find emails in CSV that don't exist in Excel
emails_not_in_excel = emails_csv - emails_excel

# Display or save the result
print("Emails not in Excel file:")
print(emails_not_in_excel)

# If you want to save the result to a new CSV file
result_df = pd.DataFrame({'email_column_name': list(emails_not_in_excel)})
result_df.to_csv('G:/results100.csv', index=False)

