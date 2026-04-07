import csv
from itertools import islice
from tracker import track
from clients import *

class CsvReader:
    
    def __init__(self, file_path, **kvargs):
        self.file_path = file_path
        self.lines_to_skip = kvargs.get('lines_to_skip', 0)
        self.delimiter =  kvargs.get('delimiter', ";")

    def read(self):
        with open(self.file_path, newline='', encoding='UTF-8') as filecsv:
            wanted_lines = islice(filecsv, self.lines_to_skip, None)
            lettore = csv.reader(wanted_lines, delimiter=self.delimiter)
            dati = [ (linea[0], linea[1]) for linea in lettore ]

        return dati



def update(csv_reader, wsc_lambda, out_path) -> None:

    securities = csv_reader.read()
    client_args = []
    for fname, tracking_code in securities:
        p = f"{out_path}/{fname}.json"
        client_args.append([p, wsc_lambda(tracking_code)])

    for file_path, wsc_paf in client_args: 
        track( file_path, wsc_paf )



# --- ESEMPIO D'USO ---
if __name__ == "__main__":

    #lines = CsvReader('cfg/eom/re/buy/areas.csv', lines_to_skip = 1).read()
    #print(lines)
    #update(CsvReader('cfg/eod/xmil/securities.csv'), wsclient_bit, 'www/eod/xmil')
    update( CsvReader('cfg/eom/pension-funds/fondofonte.csv'), wsclient_fondofonte, 'www/eom/pension-funds' )