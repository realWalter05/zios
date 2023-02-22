from bs4 import BeautifulSoup
import re
import requests

class Scraper():
	def __init__(self, page_link):
		self.page = self.get_page(page_link)
		soup = BeautifulSoup(self.page, "html.parser")

		trs = soup.find_all("tr")[:6]
		rows = self.get_listed_rows(trs)
		self.data = self.merge_rows(rows)

	def get_listed_rows(self, rows):
		listed = []

		for row in rows:
			row_list = []
			
			tds = row.find_all("td")
			for td in tds:
				if td.find('h3', attrs={'style' : 'color:#0000FF; display:inline'}):
					only_text = td.find('h3', attrs={'style' : 'color:#0000FF; display:inline'}).text
					row_list.append(self.strip_html_txt(re.sub(" +", " ", only_text)).strip())
					continue
				row_list.append(self.strip_html_txt(re.sub(" +", " ", td.text)).strip())
			listed.append(row_list)


		return listed[2:]

	def strip_html_txt(self, text):
		return text.replace("\n", "").replace("\r", "")

	def merge_rows(self, rows):
		merged_rows = []
		i = 0
		while i < len(rows):
			multi_row = [*rows[i], *rows[i+1]]
			merged_rows.append(multi_row)
			i += 2
		return merged_rows

	def get_page(self, link):
		return requests.get(link).text


