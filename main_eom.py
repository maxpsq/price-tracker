from worker import *
from clients import *


update( CsvReader('cfg/eom/re/buy/areas.csv', 1), wsclient_immobiliare_vendita, 'www/eom/re/buy' )