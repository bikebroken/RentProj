import re
import Queue
from bs4 import BeautifulSoup
import requests

class parserUrl(threading.Thread):
	
	def __init__(self,tag):
		threading.Thread.__init__(self)
		self.tag = tag
	
	def run(self):
		while True:
			try:
				self.detail_url_parser()
			except Exception as e:
				html_queue.take_done()

	def detail_url_parser(self):
		s = html_queue.get()
		s = BeautifulSoup(s).find('ul',attrs={'class':'house-lst'})
		lis = s.find_all('li')
		l = []
		for li in lis:
			detail = li.find('h2').find('a')
			detail_href = detail['href']
			if detail_href.startswith('/zufang'):
				detail_href = '{}{}.{}{}'.format(LJ.TG,self.tag,LJ.Base_Url,detail_href)
    		zufang_queue.put(detail_href)
		html_queue.task_done()	
		
class paser(threading.Thread):
	
	def __init__(self,tag,room):
		threading.Thread.__init__(self)
		self.tag = tag
		self.room = room
		
	def run(self):
		while True:
			try:
				self.zufang_html()
			except Exception as e:
				two+html_queue.task_done()
				
	def zufang_html(self):
		h = two_html_queue.get()
		s = BeautifulSoup(h)
		re_list = []
		house_name = s.find('h1',attrs={'class':'main'}).text
		house_price = s.find('span',attrs={'class':'total'}).text
		h = h.decode('utf-8')
		house_position = re.findall(r"(?<=resblockPosition:').*(?=',)",h)
		house_area = re.findall(r"(?<=<i>面积：</i>).*(?=</p>)",h)
		house_type = re.findall(r"(?<=<i>房屋户型：</i>).*(?=</p>)",h)
		house_heigth = re.findall(r"(?<=<i>楼层：</i>).*(?=</p>)",h)
		house_face = re.findall(r"(?<=<i>房屋朝向：</i>).*(?=</p>)",h)
		house_subway = re.findall(r"(?<=<i>地铁：</i>).*(?=</p>)",h)

		re_list.append(self.tag)
		re_list.append(self.room)
		re_list.append(house_name)
		re_list.append(house_price)
		re_list.append(house_position)
		re_list.append(house_area)
		re_list.append(house_type)
		re_list.append(house_heigth)
		re_list.append(house_face)
		re_list.append(house_subway)
		
		
	

