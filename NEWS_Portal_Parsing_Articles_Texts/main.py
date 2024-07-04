import csv
from search_and_save_news import search_news_Google_NEWS
from extract_news_from_json import extract_form_json_Google_NEWS
from convert_CSV_to_Excel import convert_CSV_to_Excel
from search_url import change_url
import os

clients_info = "web_pages_info.csv"
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
            web_page_name = row['SHORT_NAME']
            search_url = change_url(web_page_name)
            search_news_Google_NEWS(search_url)
            extract_form_json_Google_NEWS(web_page_name)


def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    else:
        print(f"File '{file_path}' does not exist.")


if __name__ == "__main__":
    main()
    convert_CSV_to_Excel(database_name, output_file)
