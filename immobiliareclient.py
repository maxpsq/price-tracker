from requests import get
import json
from epoch import last_day_of_month
import traceback
import logging
from immobiliarepayload import *

QRYSEP = ','

CONTRATTO_VENDITA='1'
CONTRATTO_AFFITTO='2'

VALID_CONTRACTS=('1', '2')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
}


def _query_param_by_position(n):
    param_name=''
    match n:
        case 0:
            param_name="contract"    # 1=vendita, 2=affitto
        case 1:
            param_name="nation-id"    # country ISO code
        case 2:
            param_name="region-id"    # first 3 letters lowercase 
        case 3:
            param_name="province-id"  # Italy: uppercase 2 letters code
        case 4:
            param_name="city-id"      # internal immobiliare.it numeric identifier
        case 5:
            param_name="with-zones"   # false|true
        case _:
            raise KeyError(f"Errore: La posizione '{n}' bel parametro non è gestita.")
    return param_name            
    

def _query_builder(positional_query_values):
    q={}
    for i, v in enumerate(positional_query_values):
        qp = _query_param_by_position(i)
        q[qp] = v

    return q


def immobiliare_prezzi(query_elements=[]):
    # https://www.immobiliare.it/api-next/market-insights/prices/stats/?nation-id=IT&region-id=lom&province-id=PV&city-id=8271&with-zones=false&contract=1
    url=f"https://www.immobiliare.it/api-next/market-insights/prices/stats/"
    path_and_query = _query_builder(query_elements)
    try:
        payload = ImmobiliarePayload(**path_and_query)
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

def _add_contract_to_query_elements(contract, query_elements_csv):
    all_query_elements_csv = contract + QRYSEP + query_elements_csv
    return all_query_elements_csv.split(QRYSEP)


def immobiliare_prezzi_vendita(query_elements_csv):
    query_elements = _add_contract_to_query_elements(CONTRATTO_VENDITA, query_elements_csv)
    return immobiliare_prezzi(query_elements)


def immobiliare_prezzi_affitto(query_elements_csv):
    query_elements = _add_contract_to_query_elements(CONTRATTO_AFFITTO, query_elements_csv)
    return immobiliare_prezzi(query_elements)




# --- ESEMPIO D'USO ---
if __name__ == "__main__":
    data = immobiliare_prezzi_vendita('IT,lom,PV,8271')
    print( json.dumps(data) )
