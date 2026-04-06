from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

def get_tomorrow_midnight_epoch(zi: ZoneInfo):
    """
    Ritorna lo Unix timestamp relativo alle 00:00:00 
    della data odierna nel fuso orario di Roma.
    """
    
    # Otteniamo il momento attuale nel fuso orario di Roma
    tomorrow = datetime.now(zi) + timedelta(days=1)
    
    # "Resettiamo" l'orario alle 00:00:00.000
    midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Convertiamo in timestamp Unix (intero)
    return int(midnight.timestamp())    


def date_to_unix_epoch(date_string: str) -> int:
    """
    Converte una stringa YYYY-MM-DD in Unix Epoch time (secondi).
    Assume che la data si riferisca all'inizio del giorno (00:00:00) UTC.
    """
    try:
        # 1. Trasforma la stringa in un oggetto datetime
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        
        # 2. Specifica che la data è in formato UTC (evita offset locali)
        date_obj = date_obj.replace(tzinfo=timezone.utc)
        
        # 3. Ritorna il timestamp come intero
        return int(date_obj.timestamp())
    
    except ValueError:
        raise ValueError("Formato data non valido. Usa YYYY-MM-DD")


def last_day_of_month(year, month):
    last_days = [31, 30, 29, 28]
    for day in last_days:
        try:
            end = datetime(year, month, day)
        except ValueError:
            continue
        else:
            return end.date()
    return None


# --- ESEMPIO D'USO ---
if __name__ == "__main__":
    data_test = "2026-04-05"
    epoch = date_to_unix_epoch(data_test, ZoneInfo("Europe/Rome"))
    
    print(f"La data {data_test} corrisponde all'Epoch: {epoch}")
