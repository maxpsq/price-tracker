from requests import get
import re
from itertools import batched
from bs4 import BeautifulSoup
from epoch import last_day_of_month
import traceback
import logging

VALID_ENDPOINTS = (
    'monetario-plus',
    'reddito',
    'crescita',
    'sicurezza',
    'comparto-sicurezza'
)

def url(comparto):
    if comparto not in VALID_ENDPOINTS:
        raise ValueError(f'Unknown end-point "{comparto}".')
    return f"https://www.cometafondo.it/andamenti/{comparto}/"



def fondo_cometa(comparto: str):

    TABLE_ID_PATTERN = {
        'monetario-plus'    : '^table_6_row_[0-9]+',
        'reddito'           : '^table_27_row_[0-9]+',
        'crescita'          : '^table_9_row_[0-9]+',
      # 'sicurezza'         : '^table_14_row_[0-9]+',
        'comparto-sicurezza': '^table_11_row_[0-9]+'
    }

    def get_table_records(re_pattern):
        return lambda tag: tag.name == 'tr' and tag.get('id') is not None and re.match(re_pattern, tag.get('id') )

    try:
        re_pattern = TABLE_ID_PATTERN.get(comparto)
        response = get( url(comparto) )
        soup = BeautifulSoup(response.text, 'html.parser')
        entries = []
        for tr in soup.find_all( get_table_records(re_pattern) ):
            for month, quote, _ in batched( tr.find_all('td'), n=3 ):
                if month is not None:
                    m_y = re.split('/', month.get_text())
                    d = f"{last_day_of_month( int(m_y[1]), int(m_y[0]) ):%Y-%m-%d}" 
                    q = float( quote.get_text().strip().replace(',', '.') )
                    entries.append([d, q])
        return entries

    except (Exception) as e:
        logging.error(traceback.format_exc())



# --- ESEMPIO D'USO ---
if __name__ == "__main__":
    data = fondo_cometa('comparto-sicurezza')
    print( data )