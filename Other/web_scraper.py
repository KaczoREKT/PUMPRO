import re

import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import csv

def main():
    # Ściąganie danych ze strony hebe do csv
    base_url = 'https://www.hebe.pl/pielegnacja-wlosow-szampony/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    page, prod_num = 0, 0

    with open('produkty_hebe.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'nazwa', 'cena', 'skladniki', 'url'])

        while True:
            url = f'{base_url}?start={page * 24}'
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print('waaa')
                break

            soup = BeautifulSoup(response.text, 'lxml')
            products = soup.find_all('div', class_='product-tile')

            if not products:
                print('Koniec stron.')
                break

            print(f'\nStrona {page + 1}: Znaleziono {len(products)} produktów.\n')

            for product in products:
                name_tag = product.find('a', class_='product-tile__name')
                name_text = name_tag.text.strip() if name_tag else 'Brak nazwy'

                price_tag = product.find('span', class_='price-tile__amount')
                price = price_tag.text.strip() if price_tag else 'Brak ceny'

                link_tag = product.find('a', class_='product-tile__image')
                if not link_tag or 'href' not in link_tag.attrs:
                    continue

                product_url = "https://www.hebe.pl" + link_tag['href']

                sleep(1 / randint(1, 3))
                product_response = requests.get(product_url, headers=headers)

                if product_response.status_code == 200:
                    product_soup = BeautifulSoup(product_response.text, 'lxml')
                    ingredients_tag = product_soup.find(
                        'div',
                        class_='js-navbar-section product-container__section',
                        id='product-ingredients'
                    )
                    ingredients = ingredients_tag.get_text(strip=True) if ingredients_tag else 'Brak informacji o składnikach'
                else:
                    ingredients = 'Błąd ładowania'

                # Usuwa niepotrzebny tekst z danych
                remove_phrases = ['Rozwiń i dowiedz się więcejZwiń', 'Rozwiń i dowiedz się więcej', 'Zwiń', "Składniki"]
                pattern = '|'.join(map(re.escape, remove_phrases))  # Tworzy wzór do usunięcia wszystkich fraz

                # Zastępuje wszystkie frazy i nowe linie jednym wywołaniem
                ingredients = re.sub(pattern, '', ingredients)  # Usuwa niepotrzebne frazy
                ingredients = re.sub(r'\n+', ' ', ingredients)  # Zamienia wszystkie nowe linie na spacje

                writer.writerow([prod_num, name_text, price, ingredients, product_url])
                print(f'Zapisano produkt ID {prod_num}: {name_text}')
                prod_num += 1

            page += 1
            sleep(0.3 / randint(1, 30))

if __name__ == '__main__':
    main()
