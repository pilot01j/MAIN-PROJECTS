import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import json
import time
import random


# Acces Google pages and extract all information about company , from all pages and save it to articles_list.json
def search_news_Google_NEWS(search_url):
    # Mechanism to avoid MaxRetryError
    s = random.randint(25, 40)
    time.sleep(s)
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/106.0.0.0 Safari/537.36'}
    print(search_url)
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    try:
        response = session.get(search_url, headers=headers)
        response.raise_for_status()
        # print(response.status_code)

        # if error 429 occurred set time.sleep n-second before to try again
        if response.status_code == 429:
            time.sleep(360)  # Can change the num of second if it's not enough to avoid 429 error
            return search_news_Google_NEWS(search_url)

        soup = BeautifulSoup(response.text, 'html.parser')
        check_element = soup.find('div', class_="MjjYud")
        # print(check_element)

        if check_element:
            print("Articles were found.", )
            articles = soup.find_all('div', class_="SoaBEf")
            # print(articles)

            # Read existing articles and append new
            existing_data = []
            try:
                with open('articles_list.json', 'r') as file:
                    existing_data = json.load(file)
            except FileNotFoundError or json.decoder.JSONDecodeError:
                pass
            for article in articles:
                existing_data.append({'article_html': str(article)})
            with open('articles_list.json', 'w') as file:
                json.dump(existing_data, file, indent=4)

            # Moving to the next page and using the new url to extract articles
            next_page_link = soup.find("a", id="pnnext")
            if next_page_link:
                search_url = "https://www.google.com" + next_page_link["href"]
                print("Next page:", search_url)
                search_news_Google_NEWS(search_url)
            else:
                print("There is no next page available")
        else:
            print("No articles were found.")
    except requests.RequestException as e:
        print("A network error has occurred:", e)
        time.sleep(10)
        return search_news_Google_NEWS(search_url)
    except Exception as e:
        print("An error occurred:", e)

# Test
# search_news_Google_NEWS()
