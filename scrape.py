from bs4 import BeautifulSoup
import csv
import re
from time import sleep
import requests
from datetime import datetime, timedelta

csv_file = open("YahooNews.csv",'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['heading', 'date_of_post', 'snippet', 'news_source'])

def extraction(article):
	heading = article.h3.a.text

	snippet = article.find('p', class_='fz-ms').text
	temp = snippet.split('·')
	if len(temp)==1:
		snippet = temp[0].strip()
		date_of_post = datetime.today().date()
		date_of_post = date_of_post.strftime("%d/%m/%Y")
		
	else:
		date_of_post = temp[0]
	
		if 'ago' in date_of_post:
			days = int(date_of_post.split()[0])
			date_of_post = datetime.today() - timedelta(days=days)
			date_of_post = date_of_post.date()
			date_of_post = date_of_post.strftime("%d/%m/%Y")


		snippet = temp[-1].strip()
		

	# raw_link = article.h3.a['href']
	# unquoted_link = requests.utils.unquote(raw_link)
	# pattern = re.compile("RU=(.*)\/RK")
	# clean_link = re.search(pattern, unquoted_link).group(1)
	# print(clean_link)

	news_source = article.find('span', class_="lh-17").text
	
	return heading, date_of_post, snippet, news_source


name = input("search name: ")
name = name.replace(" ","+")

url = f"https://in.search.yahoo.com/search?p={name}&fr=uh3_news_web_gs&fr2=p%3Anews%2Cm%3Asa"

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


while True:

	source = requests.get(url, headers=headers).text

	soup = BeautifulSoup(source, 'lxml')
	# print(soup.prettify())



	for article in soup.find_all('div', class_="algo-sr"):
		# print(article.prettify())

		temp = extraction(article) 

		print(temp)
		csv_writer.writerow(temp)


	try:
		next_page_url = soup.find('a', class_='next')['href']
		url = next_page_url
		sleep(1)
	except Exception as e:
		break
	
csv_file.close()



