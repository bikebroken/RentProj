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
