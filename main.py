import requests
import argparse

from functions import download_txt, download_image, parse_book_page

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скачивает книги в заданном диапазоне'
    )
    parser.add_argument('-f', '--first_book', help='Номер первой книги', type=int, default=1)
    parser.add_argument('-l', '--last_book', help='Номер последней книги', type=int, default=10)
    args = parser.parse_args()

    for id_book in range(args.first_book, args.last_book):
        url_download = f"https://tululu.org/txt.php?id={id_book}"
        response = requests.get(url_download)
        response.raise_for_status()

        if not response.history:

            url_name = f'https://tululu.org/b{id_book}'
            book_page = requests.get(url_name)
            book_page.raise_for_status()

            filename = f"{id_book}. {parse_book_page(book_page)['title']}"
            print(filename)
            # download_txt(response, f"{id_book}. {parse_book_page(book_page)['title']}", folder='books/')
            #
            # download_image(parse_book_page(book_page)['img_url'],
            #                (parse_book_page(book_page)['filename_img']), folder='foto/')
            #
            # comments = parse_book_page(book_page)['comments']
            #
            # type_books = parse_book_page(book_page)['types_book']

