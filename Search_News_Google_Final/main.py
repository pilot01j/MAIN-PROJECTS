import csv
from search_and_save_news import search_news_Google_NEWS
from extract_news_from_json import extract_form_json_Google_NEWS
from convert_CSV_to_Excel import convert_CSV_to_Excel
from search_url import change_url
import os
import asyncio

clients_info = "clients_info.csv"
database_name = 'database.csv'
output_file = 'output_file.xlsx'
json_file = "articles_list.json"


def main():
    with open(clients_info, newline='') as csvfile:
        delete_file_if_exists(json_file)
        delete_file_if_exists(database_name)
        delete_file_if_exists(output_file)
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_name = row['SHORT_NAME'].replace('?', '')
            company_search_name = row['SEARCH_NAME']
            fiscal_code = row['LEGAL_ID']
            search_url = change_url(company_search_name)
            search_news_Google_NEWS(search_url)
            extract_form_json_Google_NEWS(company_name, fiscal_code)


def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    else:
        print(f"File '{file_path}' does not exist.")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    convert_CSV_to_Excel(database_name, output_file)
