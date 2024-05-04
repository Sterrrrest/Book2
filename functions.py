import requests
import os

from environs import Env
from bs4 import BeautifulSoup
from pathlib import Path
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse

env = Env()
env.read_env()
location = env('PATH')


def download_txt(response, filename, folder='books/'):
    path = f"{folder}"
    Path(path).mkdir(parents=True, exist_ok=True)
    filename = os.path.join(f'{folder}{sanitize_filename(filename)}.txt')

    with open(filename, 'wb') as file:
        file.write(response.content)

    return filename


def download_image(img_url, filename, folder='foto/'):

    Path(f"{folder}").mkdir(parents=True, exist_ok=True)
    response = requests.get(img_url)
    response.raise_for_status()

    with open(f"{folder}{filename}", 'wb') as file:
        file.write(response.content)


def parse_book_page(page):
    page_soup = BeautifulSoup(page.text, 'lxml')

    img_tag = page_soup.find('div', class_='bookimage').find('img')['src']
    book_img_url = urljoin('https://tululu.org', img_tag)
    filename_img = sanitize_filename(urlparse(book_img_url).path.split('/')[-1])

    type_books_tags = page_soup.find('span', class_='d_book').find_all('a')
    type_books = [book_type.text for book_type in type_books_tags]

    comments_tag = page_soup.find_all('div', class_='texts')
    comments = [comment.text.split(')')[-1] for comment in comments_tag]

    book = {'title': page_soup.find('h1').text.split('::')[0].strip(),
            'author': page_soup.find('h1').text.split('::')[1].strip(),
            'img_url': book_img_url,
            'filename_img': filename_img,
            'types_book': type_books,
            'comments': comments}

    return book

