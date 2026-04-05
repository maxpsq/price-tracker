from datetime import datetime, date
from zoneinfo import ZoneInfo
import re
import json
from epoch import *
import traceback
import logging

BORSA_ITALIANA_TZI = ZoneInfo("Europe/Rome")


class Payload:
    # Lista delle chiavi ammesse
    VALID_KEYS = (
        'SampleTime', 'TimeFrame', 'RequestedDataSetType', 
        'ChartPriceType', 'Key', 'Offset', 'FromDate', 
        'ToDate', 'UseDelay', 'KeyType', 'KeyType2', 'Language'
    )

    def __init__(self, code, market, **kwargs):
        """
        Il costruttore accetta code, market e un numero variabile di parametri 
        sotto forma di key=value (kwargs).
        """
        self.code = code
        self.market = market

        tomorrow = get_tomorrow_midnight_epoch(BORSA_ITALIANA_TZI)

        self._defaults = {
            'SampleTime': "1d",
            'TimeFrame': "5y",
            'RequestedDataSetType': "ohlc",
            'ChartPriceType': "price",
            'UseDelay': False,
            'KeyType': "Topic",
            'KeyType2': "Topic",
            'Language': "en-US",
            'Offset': 0,
            'FromDate': None,
            'ToDate': None
        }

        # Dizionario dei validatori (mappa ogni chiave alla sua funzione di controllo)
        self._validators = {
            'SampleTime'    : lambda v: v == "1d",
            'TimeFrame'     : lambda v: v in ("1d", "1m", "3m", "6m", "1y", "3y", "5y"),
            'RequestedDataSetType': lambda v: v == "ohlc",
            'ChartPriceType': lambda v: v == "price",
            'UseDelay'      : lambda v: v in (False, True),
            'KeyType'       : lambda v: v == "Topic",
            'KeyType2'      : lambda v: v == "Topic",
            'Language'      : lambda v: v in ("en-US", "it-IT"),
            'Key'           : lambda v: re.match('^.+\\..+$', v),
            'Offset'        : lambda v: v >= 0,
            'FromDate'      : lambda v: v is None or isinstance(v, int) or v >= 0 or v <= tomorrow,
            'ToDate'        : lambda v: v is None or isinstance(v, int) or v >= 0 or v <= tomorrow
        }
        # Costruzione del payload
        payload = kwargs.copy()
        payload['Key'] = code + "." + market
        self._normalize_date_range_limit(payload, 'FromDate')
        self._normalize_date_range_limit(payload, 'ToDate')
        payload = self._set_payload_defaults(payload)
        # Validazione e assegnazione dei dati
        self.data = self._validate_payload(payload)

    def _normalize_date_range_limit(self, payload, key) -> None:
        try:
            value = payload[key] 
            if value and isinstance(value, date):
                value = value.strftime("%Y-%m-%d")
            elif value and isinstance(value, datetime):
                value = value.strftime("%Y-%m-%d")
            
            if isinstance(value, str):
                if value == "":
                    del payload[key]
                else:
                    payload[key] = date_to_unix_epoch(value)
        #    else:
        #        del payload[key]
        except KeyError:
            pass


    def _set_payload_defaults(self, data):
        data_and_defaults = {}
        for key in self.VALID_KEYS:
            data_and_defaults[key] = data.get(key, self._defaults.get(key)) 
        
        return data_and_defaults

    def _validate_payload(self, data):
        # Esempio con Valore Errato (ValueError)
        # p3 = Payload(code="MSFT", market="US", TimeFrame="10y")
        validated_data = {}

        for key, value in data.items():
            # 1. Verifica se la chiave è presente in VALID_KEYS
            if key not in self.VALID_KEYS:
                raise KeyError(f"Errore: La chiave '{key}' non è consentita.")
            
            # 2. Verifica il valore attraverso la funzione nel dizionario
            validator = self._validators.get(key)
            if validator and not validator(value):
                raise ValueError(f"Errore: Valore '{value}' non valido per la chiave '{key}'.")
            
            validated_data[key] = value
            
        return validated_data
    
    def json(self):
        return {'request': self.data}

    def __repr__(self):
        return f"Payload(code={self.code}, market={self.market}, data={self.data})"

# --- ESEMPI D'USO ---
if __name__ == "__main__":
    try:
        # Esempio Corretto
        p1 = Payload(
            code="XS2419364653", 
            market="MOT", 
            TimeFrame="1y",
            FromDate=""
        )
        print(p1.json())

        # Esempio con Valore Errato (ValueError)
        # p3 = Payload(code="MSFT", market="US", TimeFrame="10y")

    except (Exception) as e:
        logging.error(traceback.format_exc())