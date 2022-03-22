import datetime
from bs4 import BeautifulSoup
import requests

url = 'http://apl.utfpr.edu.br/extensao/certificados/listaPublica'
year=2013
now = datetime.datetime.now()

# event_names = []

# while(year<=now.year):
# 	_params = {'txtAno' : year}
# 	html_doc = requests.post(url, data=_params)

# 	soup = BeautifulSoup(html_doc.text, 'html.parser')

# 	select = soup.find('select', {'class' : 'combo', 'name': 'txtEvento'})
# 	for option in select.stripped_strings:
# 		event_names.append(option)
# 	year+=1

# # event_names.remove('Todos')

# print(event_names)
_params = {'txtEvento' : '6679'}
html_doc = requests.post(url, data=_params)
soup = BeautifulSoup(html_doc.text, 'html.parser')
tags_tr = soup.find_all('tr')

# remover cabeçalho
tags_tr.pop(0)

for person in tags_tr:
	tags_tds = person.find_all('td')
	name = tags_tds[0].text.strip() 
	certificate = tags_tds[1].text.strip() 
	certificate_link = person.find_all('a', href=True) 
	print(name)
	print(certificate)
	print(certificate_link[0]['href'])
	print('\n')