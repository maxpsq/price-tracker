from worker import *
from clients import *



update(CsvReader('cfg/eod/xmil/securities.csv'), wsclient_bit, 'www/eod/xmil')
