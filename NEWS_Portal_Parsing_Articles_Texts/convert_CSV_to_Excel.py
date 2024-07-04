import pandas as pd
import os


def convert_CSV_to_Excel(csv_file, output_excel):
    # Check if the output file already exists, if yes, delete it
    if os.path.exists(output_excel):
        os.remove(output_excel)

    # read CSV file
    df = pd.read_csv(csv_file, encoding='utf-8', header=None)
    # Insert column names to excel file
    df.columns = ['publication_date', 'source_name', 'source', 'title','text', 'link']

    # Convert 'publication_date' column to datetime type
    df['publication_date'] = pd.to_datetime(df['publication_date'], format='%d.%m.%Y')

    # Save DataFrame to Excel File
    df.to_excel(output_excel, index=False)


# # # Test
# convert_CSV_to_Excel('database.csv', 'output_file.xlsx')
