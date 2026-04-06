from worker import update
from clients import *



update('cfg/eod/xmil/securities.csv', wsclient_bit, 'www/eod/xmil')
