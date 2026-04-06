from  bitclient import borsa_italiana


def wsclient_bit(ws_code):
    return lambda start_since: borsa_italiana(ws_code, start_since)

