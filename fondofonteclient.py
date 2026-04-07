from requests import get
from itertools import batched
from bs4 import BeautifulSoup
from epoch import last_day_of_month
import traceback
import logging

VALID_ENDPOINTS = (
    'comparto-garantito',
    'comparto-bilanciato',
    'comparto-crescita',
    'comparto-dinamico'
)

def url(comparto):
    if comparto not in VALID_ENDPOINTS:
        raise ValueError(f'Unknown end-point "{comparto}".')
    return f"https://www.fondofonte.it/gestione-finanziaria/i-valori-quota-dei-comparti/{comparto}/"


def fondo_fonte(comparto: str):

    try:
        response = get( url(comparto) )
        soup = BeautifulSoup(response.text, 'html.parser')
        years = []
        for h5 in soup.find_all('h5'):
            years.append( int( h5.get_text() ) )

        quotes_history = {}
        for index, div in enumerate( soup.find_all('div','toggle-content-column') ):
            quotes_history[years[index]] = []
            cnt = 0
            for month, quote in batched( div.find_all('span'), n=2):
                if cnt > 0:
                    m = _month_to_number( month.get_text().strip() )
                    # Possono essere presenti delle note di testo all'interno
                    # di tag <span> fra gli elementi delle quotazioni.
                    if m is None:
                        continue
                    d = f"{last_day_of_month(years[index], m):%Y-%m-%d}"
                    q = float( quote.get_text().strip().replace(',', '.') )
                    quotes_history[years[index]].append( [ d, q ] ) 
                cnt += 1

        entries = []
        for _, list in reversed(quotes_history.items()):
            for t in reversed(list):
                entries.append(t)

        return entries

    except (Exception) as e:
        logging.error(traceback.format_exc())


def _month_to_number(month_as_word):
    convert = {
        'gennaio'   : 1,
        'febbraio'  : 2,
        'marzo'     : 3,
        'aprile'    : 4,
        'maggio'    : 5,
        'giugno'    : 6,
        'luglio'    : 7,
        'agosto'    : 8,
        'settembre' : 9,
        'ottobre'   :10,
        'novembre'  :11,
        'dicembre'  :12
    }
    return convert.get( month_as_word.lower() )



# --- ESEMPIO D'USO ---
if __name__ == "__main__":
    data = fondo_fonte('comparto-crescita')
    print( data )