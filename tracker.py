import json
from  borsaitaliana import borsa_italiana
import traceback
import logging

def track(file_path, ws_client):
    """
    Read the price data set from a file and ask a web service
    to provide the prices starting from the last date found.
    New prices are then written back to the file.
    """

    data_dict = {}          # A dict structure meant for merging data
    last_closing = None     # Las closing day found in the file
    file = None             # A file object
    try:
        file = open(file_path, "r")
        text = file.read()
        # empty file is 1 byte in size
        if len(text) > 1:
            json_dict = json.loads(text)
            for date, price in json_dict:
                data_dict[date] = price
                last_closing = date

            #last_closing = json_dict[-1][0]
    except FileNotFoundError:
        pass
    finally:
        if file is not None:
            file.close()

    new_data = ws_client(last_closing)  # New data from the data provider

    for date, price in new_data:
        data_dict[date] = price

    data_list = []                      # The final data structure to be written on disk
    for date, price in data_dict.items():
        data_list.append([date, price])

    file = None
    try:
        file = open(file_path, "w")
        file.write(json.dumps(data_list))
    except (Exception) as e:
        logging.error(traceback.format_exc())
    finally:
        if file is not None:
            file.close()



# --- ESEMPIO D'USO ---
if __name__ == "__main__":
#    code='DE0001102408'
#    market='MOT'
    p = "www/eod/xmil/XS2579483319.json"
    c = 'XS2579483319.MOT'

    def wsc(ws_code):
        return lambda start_since: borsa_italiana(ws_code, start_since)
    
    track( p, wsc(c) )
