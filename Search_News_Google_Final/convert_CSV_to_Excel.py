import pandas as pd
import os


def transform_int_to_str(cod_fiscal):
    return str(cod_fiscal)


def convert_CSV_to_Excel(csv_file, output_excel):
    # Check if the output file already exists, if yes, delete it
    # if os.path.exists(output_excel):
    #     os.remove(output_excel)

    # read CSV file
    df = pd.read_csv(csv_file, encoding='utf-8', header=None)

    # Insert column names to excel file
    df.columns = ['publication_date', 'article_type', 'fiscal_code', 'company_name', 'source', 'title', 'link']

    # Transform "fiscal_code" from int to String
    df['fiscal_code'] = df['fiscal_code'].apply(transform_int_to_str)

    # Convert 'publication_date' column to datetime type
    df['publication_date'] = pd.to_datetime(df['publication_date'], format='%d.%m.%Y')

    # sort table - order by publication_date DESC
    df.sort_values(by='publication_date', ascending=False, inplace=True)

    # Save DataFrame to Excel File
    df.to_excel(output_excel, index=False)


# # Test
# convert_CSV_to_Excel('database.csv', 'output_file.xlsx')
