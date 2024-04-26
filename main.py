import requests
import os
from pathlib import Path

path = "/Users/sterr/Documents/Python/Books/books"
Path(path).mkdir(parents=True, exist_ok=True)

for i in range(10):
    url = f'https://tululu.org/txt.php'
    payLoad = {'id': i+1}
    response = requests.get(url, params=payLoad)
    response.raise_for_status()
    if not response.history:
        filename = f'books/id{i}.txt'
        with open(filename, 'wb') as file:
            file.write(response.content)
