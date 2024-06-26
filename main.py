import requests
import argparse
import time

from functions import download_txt, download_image, parse_book_page, check_for_redirect

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Скачивает книги в заданном диапазоне'
    )
    parser.add_argument('-f', '--first_book', help='Номер первой книги', type=int, default=1)
    parser.add_argument('-l', '--last_book', help='Номер последней книги', type=int, default=10)
    args = parser.parse_args()

    for book_id in range(args.first_book, args.last_book):
        url_download = "https://tululu.org/txt.php"
        payLoad = {'id': f'{book_id}'}
        try:
            response = requests.get(url_download, params=payLoad)
            response.raise_for_status()
            check_for_redirect(response)
            book_id_url = f'https://tululu.org/b{book_id}'
            book_page = requests.get(book_id_url)
            book_page.raise_for_status()
            download_txt(response, f"{book_id}. {parse_book_page(book_page)['title']}", folder='books/')
            download_image(parse_book_page(book_page)['img_url'], folder='foto/')
        except requests.HTTPError:
            print('Error: No such book_id.')
        except requests.ConnectionError:
            print('A Connection error occurred.')
        time.sleep(60)



