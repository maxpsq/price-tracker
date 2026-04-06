import re
import traceback
import logging
import requests

class ImmobiliarePayload:

    VALID_KEYS = ('__lang', 'path')

    REGIONE=(
        'valle-d-aosta',
        'piemonte',
        'liguria',
        'lombardia',
        'veneto',
        'trentino-alto-adige',
        'friuli-venezia-giulia',
        'emilia-romagna',
        'toscana',
        'umbria',
        'marche',
        'lazio',
        'abruzzo',
        'campania',
        'molise',
        'puglia',
        'sardegna',
        'sicilia',
        'calabria',
        'basilicata'
    )

    def __init__(self, **kwargs):
        """
        Il costruttore accetta code, market e un numero variabile di parametri 
        sotto forma di key=value (kwargs).
        """

        self._defaults = {
            '__lang': "en"
        }

        # Dizionario dei validatori (mappa ogni chiave alla sua funzione di controllo)
        self._validators = {
            '__lang'        : lambda v: isinstance(v, str) and v in ("de", "el", "en", "es", "fr", "it", "pt", "ru"),
            'path'          : lambda v: isinstance(v, str) and re.match('^/[a-z-]+/[a-z-]+/[a-z-]+/$', v)
        }

        self._post_processors = {
        }
        # Costruzione del payload
        payload = kwargs.copy()
        payload = self._set_payload_defaults(payload)
        # Validazione e assegnazione dei dati
        payload = self._validate_payload(payload)
        payload = self._post_process_payload(payload)
        self.data = payload

    def _set_payload_defaults(self, data):
        data_and_defaults = {}
        for key in self.VALID_KEYS:
            data_and_defaults[key] = data.get(key, self._defaults.get(key)) 
        
        return data_and_defaults

    def _validate_payload(self, data):
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
    
    def _post_process_payload(self, data):
        post_processed_data = {}

        for key, value in data.items():
            
            # 2. Verifica il valore attraverso la funzione nel dizionario
            post_processor = self._post_processors.get(key, None)
            if post_processor is not None:
                value = post_processor(value)

            post_processed_data[key] = value
            
        return post_processed_data
    
    def payload(self):
        return self.data

    def __repr__(self):
        return f"Payload(code={self.code}, market={self.market}, data={self.data})"



# --- ESEMPI D'USO ---
if __name__ == "__main__":
    try:
        # Esempio Corretto
        p1 = ImmobiliarePayload(
            path="/mercato-immobiliare/lombardia/landriano/"
        )
        print(p1.payload())

        # Esempio con Valore Errato (ValueError)
        # p3 = Payload(key="MSFT", TimeFrame="10y")

    except (Exception) as e:
        logging.error(traceback.format_exc())