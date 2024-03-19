import csv
from search_and_save_news import search_news_Google_NEWS
from extract_news_from_json import extract_form_json_Google_NEWS
from convert_CSV_to_Excel import convert_CSV_to_Excel
from search_url import change_url

clients_info = "clients_info.csv"
database_name = 'database.csv'
output_file = 'output_file.xlsx'


def main():
    with open(clients_info, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company_name = row['SHORT_NAME'].replace('?', '')
            company_search_name = row['SEARCH_NAME']
            fiscal_code = row['LEGAL_ID']
            search_url = change_url(company_search_name)
            search_news_Google_NEWS(search_url)
            extract_form_json_Google_NEWS(company_name, fiscal_code)


if __name__ == "__main__":
    main()
    convert_CSV_to_Excel(database_name, output_file)
