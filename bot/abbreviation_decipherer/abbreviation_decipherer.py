import random

from bs4 import BeautifulSoup
import requests
import re

ABBR_BASE_URL = "https://xn----7sbbfsshef0aedydgg4lyb.xn--p1ai"


def get_deciphers_from_abbr_page(page):
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find(id="cards-list-0")
    # поскольку на странице не сразу таблица, а только ссылка на неё, то сначала добываем url таблицы
    deciphers_raw_url = re.search(r"fetch\('\S*'\)", str(table)).group(0)[7:-2]
    deciphers_url = ABBR_BASE_URL + deciphers_raw_url
    page = requests.get(deciphers_url)
    # парсим таблицу
    soup = BeautifulSoup(page.text, "html.parser")
    p_deciphers = soup.findAll(class_="mx-2")
    deciphers = list()

    for dph in p_deciphers:
        norm_text = " ".join(dph.text.split())
        deciphers.append(norm_text)

    return deciphers


def get_deciphers(abbr):
    base_url = "https://xn----7sbbfsshef0aedydgg4lyb.xn--p1ai"
    url = f"{base_url}/a/{abbr}"
    main_abbr_page = requests.get(url)

    if main_abbr_page.status_code == 200:
        deciphers = get_deciphers_from_abbr_page(main_abbr_page)
        return 1, abbr, deciphers
    elif main_abbr_page.status_code == 404:
        search_url = f"{base_url}/s?q={abbr}"
        search_page = requests.get(search_url)
        soup = BeautifulSoup(search_page.text, "html.parser")
        groups = soup.find_all(class_="list-group")
        if len(groups) == 0:
            # если вообще ничего не нашли, то возвращаем пустой список
            return -1, None, list()

        imprecise_matches = groups[1].find_all(class_="list-group-item")
        # берём ссылку на случайную подходящую аббревиатуру
        imprecise_abbr_href = random.choice(imprecise_matches)["href"]
        imprecise_abbr_url = ABBR_BASE_URL + imprecise_abbr_href
        imprecise_abbr_page = requests.get(imprecise_abbr_url)
        deciphers = get_deciphers_from_abbr_page(imprecise_abbr_page)
        new_abbr = imprecise_abbr_href.split("/")[-1]
        return 0, new_abbr, deciphers
    else:
        assert ValueError(f"abbr: {abbr}\n code: {main_abbr_page.status_code}")
    # print(imprecise_matches[0]["href"])
    # return deciphers


if __name__ == "__main__":
    abbr = "лол"
    print(get_deciphers(abbr))
