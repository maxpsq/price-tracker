from requests import get
import json
from epoch import last_day_of_month
import traceback
import logging
from immobiliarepayload import *

CONTRATTO=('1', '2')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
}

def _path_builer(path_elements):
    path="/"
    for e in path_elements:
        path += e.replace(' ', '-').replace("'", '-')
        path += "/"

    return path


def immobiliare_prezzi(contratto: str, path_elements=[]):
    url=f"https://www.immobiliare.it/api-next/city-guide/price-chart/{contratto}/"
    query_path = "/mercato-immobiliare" + _path_builer(path_elements)
    try:
        payload = ImmobiliarePayload(path=query_path)
        response = get( url, headers=HEADERS, params=payload.payload() )
        entries = []
        labels = json.loads( response.text ).get('labels')
        values = json.loads( response.text ).get('values')
        for label, value in zip(labels, values):
            y, m, _ = label.split('-')
            date = f"{last_day_of_month( int(y), int(m) ):%Y-%m-%d}"
            close = float(value)
            entries.append( [date, close] )

        return entries

    except (Exception) as e:
        logging.error(traceback.format_exc())


def immobiliare_prezzi_vendita(path_elements_csv):
    path_elements = path_elements_csv.split(',')
    return immobiliare_prezzi("1", path_elements)


def immobiliare_prezzi_affitto(path_elements_csv):
    path_elements = path_elements_csv.split(',')
    return immobiliare_prezzi("2", path_elements)




# --- ESEMPIO D'USO ---
if __name__ == "__main__":
    data = immobiliare_prezzi_vendita('lombardia,landriano')
    print( json.dumps(data) )
