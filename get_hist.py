#from binance_historical_data import BinanceDataDumper
#
#data_dumper = BinanceDataDumper(
#    path_dir_where_to_dump="data",
#    asset_class="spot",
#    data_type="klines",
#    data_frequency="1m"
#)
#data_dumper.dump_data()

import pandas as pd
import requests
from datetime import datetime, timedelta
import time
import json

def get_binance_bars(symbol, interval, startTime, endTime):
    url = "https://api.binance.com/api/v3/klines"

    startTime = str(int(startTime.timestamp() * 1000))
    endTime = str(int(endTime.timestamp() * 1000))
    limit = '1000'

    req_params = {"symbol" : symbol, 'interval' : interval, 'startTime' : startTime, 'endTime' : endTime, 'limit' : limit}

    df = pd.DataFrame(json.loads(requests.get(url, params = req_params).text))

    if (len(df.index) == 0):
        return None

    df = df.iloc[:, 0:6]
    df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']

    df.open      = df.open.astype("float")
    df.high      = df.high.astype("float")
    df.low       = df.low.astype("float")
    df.close     = df.close.astype("float")
    df.volume    = df.volume.astype("float")

    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')

    return df

def download_all_binance(symbol, interval, start, end):
    data = pd.DataFrame()
    current = start

    while current < end:
        new_end = min(current + timedelta(days=1), end)
        df = get_binance_bars(symbol, interval, current, new_end)

        if df is not None and not df.empty:
            data = pd.concat([data, df])
            print(f"Descargados datos desde {current} hasta {new_end}")
        else:
            print(f"No hay datos disponibles desde {current} hasta {new_end}")
        
        current = new_end
        time.sleep(1)  # Para respetar los límites de la API
    
    return data

# Ejemplo de uso
symbol = 'BTCUSDT'
interval = '1m'
start_date = datetime(2017, 8, 17)  # Fecha de inicio de Binance
end_date = datetime.now()

historical_data = download_all_binance(symbol, interval, start_date, end_date)

# Guardar los datos en un archivo CSV
historical_data.to_csv(f'{symbol}_{interval}_historical_data.csv', index=False)
print(f"Datos guardados en {symbol}_{interval}_historical_data.csv")