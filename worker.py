import csv
from bitclient import borsa_italiana
from tracker import track

def read_securities_csv(file_path):
    with open(file_path, newline="", encoding="UTF-8") as filecsv:
        lettore = csv.reader(filecsv, delimiter=";")
        # header = next(lettore)
        # print(header)
        dati = [ (linea[0], linea[1]) for linea in lettore ]

    return dati


def wsc_bit(ws_code):
    return lambda start_since: borsa_italiana(ws_code, start_since)



def run(csv_file_path, wsc_lambda, out_path) -> None:

    securities = read_securities_csv(csv_file_path)
    client_args = []
    for fname, tracking_code in securities:
        p = f"{out_path}/{fname}.json"
        client_args.append([p, wsc_lambda(tracking_code)])

    for file_path, wsc_paf in client_args: 
        track( file_path, wsc_paf )



# --- ESEMPIO D'USO ---
if __name__ == "__main__":
    run('cfg/eod/xmil/securities.csv', wsc_bit, 'www/eod/xmil')