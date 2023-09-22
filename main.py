import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36"}


def get_url():
    url = "https://цдк-созвездие.рф/category/afisha/nab-v-kollekt/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    data = soup.find_all('div', class_='mix col-md-4 col-sm-6')

    for card in data:
        posts = card.find('div', class_='ports').get('id')
        list_url_name = 'https://цдк-созвездие.рф/' + card.find('a', rel="bookmark").get('href').replace(
            'https://xn----dtbecebkckn9b9a2d.xn--p1ai/', '')
        url_img = 'https://цдк-созвездие.рф/' + card.find('img').get('src').replace(
            'https://xn----dtbecebkckn9b9a2d.xn--p1ai/', '')
        yield list_url_name, url_img, posts


file = open('list_card.json', 'w', encoding='utf-8')
for url_name, img, post in get_url():
    new = {"id": post, "img": img, "url_name": url_name}
    response = requests.get(url_name, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    new["content"] = soup.find('div', class_='entry-content').text
    json.dump(new, file, indent=2, ensure_ascii=False)
    # new.clear()
file.close()
