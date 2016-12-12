#! /usr/bin/env python
# -*- coding: utf-8 -*-
#####################################
from bs4 import BeautifulSoup
import requests
import time
import re


######################################
headers = {
	'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
	'Referer': 'http://www.ivsky.com/tupian/index_1.html'
}
url = 'http://www.ivsky.com/tupian'
img_url_list = []
cleaned_uri_list = []

#######################################
def get_links_from(url, page):
	list_pages = '{}/index_{}.html'.format(url, str(page))
	print(list_pages)
	web_data = requests.get(list_pages, headers=headers)
	soup = BeautifulSoup(web_data.text, 'lxml')
	img_url = soup.select('div.il_img > a > img')
	# time.sleep(5)


	for img in img_url:
		img_url_list.append(img.get('src'))


#######################################
def get_all_links_from(url, max_page=2):
	# 1.获取数据
	for page in range(1,max_page):
		get_links_from(url, page)
		time.sleep(3)

	# 2.清理数据
	for dirty_uri in img_url_list:
		matchObj = re.match(r'^http(s?):\/\/.*', dirty_uri)
		if matchObj:
			cleaned_uri_list.append(dirty_uri)

	# 3.保存数据
	f = open('firstapp/image_url.txt', 'w')
	for cleaned_uri in cleaned_uri_list:
		f.write(cleaned_uri)
		f.write("\n")
	f.close()


#########################################
if __name__ == '__main__':
	# 1.抓取并保存图片url数据
	get_all_links_from(url, max_page=5)

	# # 2.生成假数据
	# f = open('./image_url.txt', 'r')
	# fake = Factory.create()
	#
	# for url in f.readline():
	#     article = Article(
	#         title = fake.text(max_nb_chars=90),
	#         img = url,
	#         content = fake.text(max_nb_chars=3000),
	#         views = fake.random_digit(),
	# 		likes = fake.random_digit(),
	# 		createtime = fake.date_time_this_month(),
	#     )
	# 	print(article.title)
	# 	article.save

#########################################
