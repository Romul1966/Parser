import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 YaBrowser/23.7.5.734 Yowser/2.5 Safari/537.36"}


def check_post(id):
    with open('list_card_events.json', encoding='utf-8') as file:
        data = json.load(file)
        for k in data.keys():
            if id == k:
                return True
        return False


def get_url():
    url = "https://цдк-созвездие.рф/category/afisha/me-ropriyatiya/"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    all_card = soup.find_all("div", class_="mix col-md-4 col-sm-6")

    for card in all_card:
        post = card.find("div", class_="ports").get("id")

        img = 'https://цдк-созвездие.рф/' + card.find('img').get('src').replace(
            'https://xn----dtbecebkckn9b9a2d.xn--p1ai/',
            '')
        link = "https://цдк-созвездие.рф/" + card.find('a', rel='bookmark').get('href').replace(
            'https://xn----dtbecebkckn9b9a2d.xn--p1ai/', '')

        yield post, img, link


card_dict = {}
for post, img, link in get_url():

    if check_post(post):
        continue

    card_dict[post] = {"img": img, "link": link}

    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    content_text = soup.find('div', class_='entry-content').text
    card_dict[post]["content"] = ' '.join([i.strip() for i in content_text.split()])

    button = soup.find('a', class_="abiframelnk")
    if button is not None:
        card_dict[post]["button"] = button.get('href')



if card_dict:
    with open('list_card_events.json', encoding='utf-8') as file:
        data = json.load(file)
        for k, v in card_dict.items():
            data[k] = v
    with open('list_card_events.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
