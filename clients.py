from bitclient import borsa_italiana
from immobiliareclient import immobiliare_prezzi_vendita, immobiliare_prezzi_affitto

def wsclient_bit(ws_code):
    return lambda start_since: borsa_italiana(ws_code, start_since)


def wsclient_immobiliare_vendita(ws_code):
    return lambda start_since: immobiliare_prezzi_vendita(ws_code)

def wsclient_immobiliare_affitto(ws_code):
    return lambda start_since: immobiliare_prezzi_affitto(ws_code)