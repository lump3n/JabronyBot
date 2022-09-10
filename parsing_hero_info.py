import requests
from bs4 import BeautifulSoup


def get_html(url):
    """ Функция собирает html код по заданному url адресу """

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'
                             'AppleWebKit/537.36 (HTML, like Gecko)'
                             'Chrome/35.0.1916.47 Safari/537.36'}
    html_code = requests.get(url=url, headers=headers)
    html_code.encoding = 'utf-8'
    return html_code


def get_data(html_table):
    """ Функция находит данные винрейтов и имен героев в html коде и заносит их в списки """

    headers = html_table.find('header').text

    data_values = []
    for td in html_table.find_all('td'):
        data_values.append(td.text)
    data_values = list(filter(None, data_values))

    filtered_data_values = []
    for i in range(5):
        filtered_data_values.append([data_values[::3][i], data_values[2::3][i]])

    return headers, filtered_data_values


def get_list_of_hero_name(r):
    """ Функция находит список всех существующих героев """
    soup = BeautifulSoup(r.text, 'html.parser')
    href_div = soup.find('div', class_='hero-grid')

    href_a = href_div.find_all('a', href=True)
    hrefs = []
    for i in href_a:
        hrefs.append(i.get('href')[i.get('href').rfind('/') + 1:len(i.get('href'))])

    choices = []
    for hih in hrefs:
        choices.append(hih)

    return choices


def get_img_links(r):
    url2 = 'https://ru.dotabuff.com'
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find(class_='counter-outline')
    body = div.find('tbody')
    ava = body.find_all('img', class_='image-avatar')

    heh = [url2 + img.get('src') for img in ava]

    return heh


def get_img(img_link):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'
                             'AppleWebKit/537.36 (HTML, like Gecko)'
                             'Chrome/35.0.1916.47 Safari/537.36'}

    return requests.get(img_link, stream=True, headers=headers)


def parse(url: str):
    """ Главная функция парсера  """
    html = get_html(url).text
    soup = BeautifulSoup(html, 'html.parser')

    avatar_src = soup.find('img', class_='image-avatar image-hero').get('src')

    html_table = soup.find(class_='counter-outline')
    table_headers, table_data = get_data(html_table)

    return table_headers, table_data, avatar_src
