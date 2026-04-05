from requests import post
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import traceback
import logging
from payload import Payload

URL = 'https://charts.borsaitaliana.it/charts/services/ChartWService.asmx/GetPricesWithVolume'

HEADERS = {
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept": "application/json, text/javascript, */*; q=0.01", 
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3", 
    "Referer": "https://charts.borsaitaliana.it/charts/Bit/DetailedChart.aspx?mcode=TIT.I06613.TLX&lang=en",
    "X-Requested-With": "XMLHttpRequest", 
#-H "Content-Length: 236",
    "Origin": "https://charts.borsaitaliana.it",
    "DNT": "1",
    "Alt-Used": "charts.borsaitaliana.it",
    "Connection": "keep-alive", 
    "Sec-Fetch-Dest": "empty", 
    "Sec-Fetch-Mode": "cors", 
    "Sec-Fetch-Site": "same-origin", 
    "TE": "trailers"
}

def borsa_italiana(isin, market, from_date: str):

    try:

        payload = Payload(
            code=isin, 
            market=market, 
            TimeFrame="5y",
            FromDate=from_date
        )
        response = post( URL, headers=HEADERS, json=payload.json() )
        #print( response.text)
        entries = []
        elems = json.loads( response.text ).get('d')
        #exit()
        for epoch, _, _, close, _, _, _ in elems:
            date = f"{datetime.fromtimestamp( epoch/1000, tz=ZoneInfo("Europe/Rome") ):%Y-%m-%d}"
            entries.append( [date, close] )

        return entries


    except (Exception) as e:
        logging.error(traceback.format_exc())


# --- ESEMPIO D'USO ---
if __name__ == "__main__":
    # XS2419364653
    # XS2579483319
    # XS1696445516
    # DE0001102408
    data = borsa_italiana('XS2419364653','MOT', '2026-03-31')
    print( json.dumps(data) )

"""
https://forum.portfolio-performance.info/t/how-can-i-track-certificates/20393/2

curl -d '{"request":{"SampleTime":"1d","TimeFrame":"1y","RequestedDataSetType":"ohlc","ChartPriceType":"price","Key":"I06613.TLX","OffSet":0,"FromDate":null,"ToDate":null,"UseDelay":false,"KeyType":"Topic","KeyType2":"Topic","Language":"en-US"}}' -H "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0" -H "Accept: application/json, text/javascript, */*; q=0.01" -H "Accept-Language: de,en-US;q=0.7,en;q=0.3" -H "Accept-Encoding: gzip, deflate, br" -H "Referer: https://charts.borsaitaliana.it/charts/Bit/DetailedChart.aspx?mcode=TIT.I06613.TLX&lang=en" -H "Content-Type: application/json; charset=utf-8" -H "X-Requested-With: XMLHttpRequest" -H "Content-Length: 236" -H "Origin: https://charts.borsaitaliana.it" -H "DNT: 1" -H "Alt-Used: charts.borsaitaliana.it" -H "Connection: keep-alive" -H "Sec-Fetch-Dest: empty" -H "Sec-Fetch-Mode: cors" -H "Sec-Fetch-Site: same-origin" -H "TE: trailers" -X POST http://charts.borsaitaliana.it//charts/services/ChartWService.asmx/GetPricesWithVolume --compressed --output XS2226707482.json

-------------------

curl -d 

'{"request":
    {"SampleTime":"1d",
     "TimeFrame":"1y",
     "RequestedDataSetType":"ohlc",
     "ChartPriceType":"price",
     "Key":"I06613.TLX",
     "OffSet":0,
     "FromDate":null,
     "ToDate":null,
     "UseDelay":false,
     "KeyType":"Topic",
     "KeyType2":"Topic",
     "Language":"en-US"
    }
}' 

-H "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0" 
-H "Accept: application/json, text/javascript, */*; q=0.01" 
-H "Accept-Language: de,en-US;q=0.7,en;q=0.3" 
-H "Accept-Encoding: gzip, deflate, br" 
-H "Referer: https://charts.borsaitaliana.it/charts/Bit/DetailedChart.aspx?mcode=TIT.I06613.TLX&lang=en" 
-H "Content-Type: application/json; charset=utf-8" 
-H "X-Requested-With: XMLHttpRequest" 
-H "Content-Length: 236" 
-H "Origin: https://charts.borsaitaliana.it" 
-H "DNT: 1" -H "Alt-Used: charts.borsaitaliana.it" 
-H "Connection: keep-alive" 
-H "Sec-Fetch-Dest: empty" 
-H "Sec-Fetch-Mode: cors" 
-H "Sec-Fetch-Site: same-origin" 
-H "TE: trailers"
-X POST http://charts.borsaitaliana.it//charts/services/ChartWService.asmx/GetPricesWithVolume


 --compressed --output XS2226707482.json


======================
 
Interessante

https://grafici.borsaitaliana.it/interactive-chart/IT0005547408-MOTX?lang=it

"""