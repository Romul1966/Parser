import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36"}


def check_post(id):
    with open('list_card.json', encoding='utf-8') as file:
        data = json.load(file)
        for k in data.keys():
            if id == k:
                return True
        return False


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

        yield posts, list_url_name, url_img


card_dict = {}
for post, url_name, img in get_url():

    if check_post(post):
        continue

    card_dict[post] = {"img": img, "url_name": url_name}

    response = requests.get(url_name, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    content_text = soup.find('div', class_='entry-content').text
    card_dict[post]["content"] = ' '.join([i.strip() for i in content_text.split()])

if card_dict:
    with open('list_card.json', 'a', encoding='utf-8') as file:
        json.dump(card_dict, file, indent=2, ensure_ascii=False)

