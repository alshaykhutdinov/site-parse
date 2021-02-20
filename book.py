import requests
from bs4 import BeautifulSoup
import csv
import os
import time

URL = input('Введите URL: ')
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36', 'accept': '*/*'}
FILE = 'book.csv'
NEXT_PAGE_PATH = '/listview/biglist/~'
HOST = 'https://www.livelib.ru'
PARSING_PAGES = 5

def get_html(url):
	r = requests.get(URL, headers=HEADERS)
	r.encoding = 'utf-8'
	return r

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('div', class_='brow-inner')
	book = []
	for item in items:
		book.append({
			'title': item.find('a', class_='brow-book-name').get_text(),
			'link': HOST + item.find('a', class_='brow-book-name').get('href'),
			'author': item.find('a', class_='brow-book-author').get_text(),
			'label': item.find('a', class_='label-genre').get_text(),
			'love': item.find('a', class_='love').get_text(),
			'rating': item.find('span', class_='rating-value').get_text(),
			})
	return book

def save_file(items, path):
	with open(path, 'w', newline='') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(['title', 'link', 'author', 'label', 'love', 'rating'])
		for item in items:
			writer.writerow([item['title'], item['link'], item['author'], item['label'], item['love'], item['rating']])


def parse():
	html = get_html(URL)
	if html.status_code == 200:
		book = []
		for page in range(1, PARSING_PAGES + 1):
			print(f'Парсинг страницы {page} из {PARSING_PAGES}...')
			if page == 1:
				html = get_html(URL)
			elif page > 1:
				next_page = URL + NEXT_PAGE_PATH + str(page)
				html = get_html(next_page)
			book.extend(get_content(html.text))
			time.sleep(2)
		save_file(book, FILE)
		print(f'Получено {len(book)} книг')
		print(f'Файл {FILE} сохранен успешно в папку c:\\code\\')
		os.startfile(FILE)
	else:
		'Error'

parse()
