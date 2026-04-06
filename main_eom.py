from worker import *
from clients import *


update( CsvReader('cfg/eom/re/buy/areas.csv', lines_to_skip = 1), wsclient_immobiliare_vendita, 'www/eom/re/buy' )