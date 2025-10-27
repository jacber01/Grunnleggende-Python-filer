import warnings
import pandas as pd
import numpy as np
import yfinance as yf  # Rettet fra "yginance" til "yfinance"
from datetime import datetime, timedelta
import os

# --- Fjerner støy fra terminalen---
warnings.filterwarnings("ignore")

# --- Konfig ---
frequency = "w" # ønsket frekvens for eksport: "d" = daglig, "w" = ukentlig, "m" = månedlig

# --- Setter datoer for nedlasting ---
end_date = datetime.now()
start_date = end_date - pd.DateOffset(years=3)  # henter data fra de siste 3 årene til dagens dato

# --- Laster ned data ---
data = yf.download("OSEBX.OL", start=start_date, end=end_date, auto_adjust = True) # laster ned OSEBX data fra Yahoo Finance, yyyy-mm-dd format

# --- Beregner nødvendige kolonner ---
data['log_return'] = np.log(data['Close'] / data['Close'].shift(1)) # beregner logaritmiske avkastninger
data['volume_zscore'] = (data['Volume'] - data['Volume'].rolling(30).mean()) / data['Volume'].rolling(30).std() # beregner z-score for volum over 30 dager
data['realized_volatility_30d'] = data['log_return'].rolling(30).std() * np.sqrt(252) # beregner realisert volatilitet over 30 dager, annualisert
data['hl_spread'] = (data['High'] - data['Low']) / data['Close'] * 100 # beregner high/low spread i prosent
data['rebased_close'] = (data['Close'] / data['Close'].iloc[0]) * 100 # standardiserer lukkekursen

# --- Klargjør data
compiled_data = data[["rebased_close","log_return", 'volume_zscore', 'realized_volatility_30d', 'hl_spread']].dropna()
compiled_data.index = pd.to_datetime(compiled_data.index)

# --- Resampler data til ønsket frekvens og eksporterer ---
freq = frequency.upper().replace("M", "ME") 

if freq == "D":
    final_data = compiled_data.copy()
else:
    final_data = compiled_data.resample(freq).last()
    final_data['log_return'] = compiled_data['log_return'].resample(freq).sum()
    final_data['volume_zscore'] = compiled_data['volume_zscore'].resample(freq).mean()
    final_data['realized_volatility_30d'] = compiled_data['realized_volatility_30d'].resample(freq).mean()
    final_data['hl_spread'] = compiled_data['hl_spread'].resample(freq).mean()
    final_data = final_data.dropna()


# --- Eksporterer til CSV ---
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "OSEBX_data.csv")
    final_data.to_csv(file_path) # eksporterer data til CSV-fil
    print("Data eksportert til OSEBX_data.csv")
except:
    print("Feil ved eksportering av data.")
