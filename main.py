import datetime
import json
import time
from bs4 import BeautifulSoup
import requests

url = ''
year = 2020
now = datetime.datetime.now()

event_ids = []

items = []

while(year <= now.year):
    _params = {'txtAno': year}
    url = 'http://apl.utfpr.edu.br/extensao/certificados/listaPublica'
    html_doc = requests.post(url, data=_params)

    soup = BeautifulSoup(html_doc.text, 'html.parser')

    select = soup.find('select', {'class': 'combo', 'name': 'txtEvento'})

    for option in select.find_all('option'):
        event_ids.append(option['value'])

    print('number of events ', len(event_ids))

    event_ids.remove('')

    for event_id in event_ids:
        if not event_id.isnumeric():
            continue

        _params = {'txtEvento': event_id}

        print('find all certificates for event id', event_id)

        while True:
            time.sleep(2)
            
            html_doc = requests.post(url, data=_params)
            soup = BeautifulSoup(html_doc.text, 'html.parser')

            title = soup.find('div', {'class': 'titulo_right'}).h3.text.replace(
                'Listagem de Certificados - ', '')

            print('event name', title)

            found_certificates = soup.find(
                'b', string='Não foram encontrados certificados válidos para emissão')

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
                certificate_link = person.find('a', href=True)['href']
                certificate_id = certificate_link.replace(
                    'http://apl.utfpr.edu.br/extensao/certificados/validar/', '')
                certificate_link_download = 'http://apl.utfpr.edu.br/extensao/emitir/' + certificate_id

                item = {'name': name, 'event_name': title, 'certificate_id': certificate_id, 'certificate_type': certificate,
                        'certificate_link_validation': certificate_link, 'certificate_link_download': certificate_link_download, 'year': year}

                items.append(item)
                # print(item)

            next_page = soup.find("a", string="Próximo")

            print('next', next_page)

            has_next_page = next_page != None
            if not has_next_page:
                break
            url = next_page['href']
            print('url next page', url)

    file_name = './dataset_'+str(year)+'.json'
    # file = open(file_name,'w+',  encoding='utf8')

    with open(file_name, 'w+') as file:
        json.dump(items, file, ensure_ascii=False)

        # reset for next year
    event_ids = []
    items = []
    year += 1

print('finished')
