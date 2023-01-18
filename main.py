from pprint import pprint
import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from time import sleep



def parser_soup(span_teg):

    find_list = []

    description = span_teg.find('div', class_='g-user-content').text
    if "Django" and "Flask" in description:
        find_span = {}
        find_span['link'] = span_teg.find('a')['href']
        try:
            find_span['salaries'] = span_teg.find('span', class_='bloko-header-section-3').text.replace('\u202f', " ")
        except AttributeError:
            find_span['salaries'] = "Not specified"
        find_span['vocation'] = span_teg.find('a').text
        find_span['city'] = span_teg.find(attrs={"data-qa": "vacancy-serp__vacancy-address"}).text.split(',')[0]
        find_span['description'] = description
        return find_span


def save_jsone(to_json):

    print("\n" "Rec to file")
    with open('parser.json', 'w', encoding='UTF-8') as file:
        json.dump(to_json, file, ensure_ascii=False)
    print("Result saved to file")



def get_req():

    list_fot_json = []
    headers = {'User-Agent':'chrome'}

    html_hh = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=headers).text
    soup = BeautifulSoup(html_hh, features='lxml')
    soup_parsers = soup.find_all('div', class_='serp-item')

    with tqdm (total = int(len(soup_parsers)), desc='Searching') as bar:
        for soup_parser in soup_parsers:
            parser_soup(soup_parser)
            if parser_soup(soup_parser) != None:
                list_fot_json.append(parser_soup(soup_parser))
                print("\n" " Match found" "\n")
            sleep(0.2)
            bar.update()
        print(" done")

    save_jsone(list_fot_json)


if __name__ == '__main__':
    get_req()
