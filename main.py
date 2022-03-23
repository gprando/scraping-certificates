import datetime
import json
from bs4 import BeautifulSoup
import requests

url = 'http://apl.utfpr.edu.br/extensao/certificados/listaPublica'
year=2013
now = datetime.datetime.now()

event_ids = []

items = []

while(year<=2014):
	_params = {'txtAno' : year}
	html_doc = requests.post(url, data=_params)

	soup = BeautifulSoup(html_doc.text, 'html.parser')

	select = soup.find('select', {'class' : 'combo', 'name': 'txtEvento'})
	for option in select.find_all('option'):
		event_ids.append(option['value'])
	year+=1

print('number of events ', len(event_ids))

event_ids.remove('')
# event_ids = ['2494']

for event_id in event_ids: 
	if not event_id.isnumeric():
		continue

	_params = {'txtEvento' : ''+event_id+''}

	print('find all certificates for event id', event_id)

	while True:
		html_doc = requests.post(url, data=_params)
		soup = BeautifulSoup(html_doc.text, 'html.parser')

		found_certificates = soup.find('b', string='Não foram encontrados certificados válidos para emissão')
		
		has_certificates = found_certificates == None
		print('has_certificates', has_certificates)
		
		if not has_certificates:
			break

		tags_tr = soup.find_all('tr')

		# remover cabeçalho
		tags_tr.pop(0)

		for person in tags_tr:

			tags_tds = person.find_all('td')
			name = tags_tds[0].text.strip() 
			certificate = tags_tds[1].text.strip() 
			certificate_link = person.find_all('a', href=True)

			item = { 'name': name, 'certificate': certificate, 'certificate_link': certificate_link[0]['href'] }

			items.append(item)
			print(item)

		next_page = soup.find("a", string="Próximo")

		print('\n\n next',next_page)

		has_next_page = next_page != None
		if not has_next_page:
			break
		url =  next_page['href']
		print('url next page', url)


file_name = './dataset.json'
# file = open(file_name,'w+',  encoding='utf8')

with open(file_name, 'w+') as file:
	json.dump(items, file, ensure_ascii=False)