import warnings
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from hmmlearn.hmm import GaussianHMM
import matplotlib.pyplot as plt

# --- Fjerner støy fra terminalen---
warnings.filterwarnings("ignore")

# --- Leser inn data fra CSV-filen ---
base = os.path.dirname(os.path.abspath(__file__))  # finner mappen der python filen ligger
file_path = os.path.join(base, "OSEBX_data.csv")   # lager full sti til CSV-filen

df = pd.read_csv(file_path, index_col=0, parse_dates=[0])  # leser inn CSV-filen
df = df[~df.index.isin(["Ticker", "Date"])]  # fjerner eventuelle ikke-dato rader
df.index = pd.to_datetime(df.index, format="%Y-%m-%d")  # sikrer at indeksen er i datetime-format

# --- Forbereder observasjonsdata ---
obs_cols = ["log_return", "realized_volatility_30d", "hl_spread", "volume_zscore"]  # observasjonskolonner
X_df = df[obs_cols].replace([np.inf, -np.inf], np.nan).dropna()  # fjerner rader med NaN eller uendelige verdier

# --- Standardiserer dataene ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_df.values)

# --- Trener HMM-modellen ---
model = GaussianHMM(
    n_components=2,
    covariance_type="full",
    n_iter=500, 
    random_state=42
)

model.fit(X_scaled)

# --- Fast overgangsmatrise ---
P = model.transmat_

# --- Predikerer skjulte tilstander ---
states = model.predict(X_scaled)
X_out = X_df.copy()
X_out["Regime"] = states

# --- Beregner gjennomsnittlig volatilitet for å identifisere regimer ---
mean_vol_by_state = X_out.groupby("Regime")["realized_volatility_30d"].mean()
turbulent_regime = mean_vol_by_state.idxmax()
rolig_regime = mean_vol_by_state.idxmin()

# --- Identifiserte regimer for varighet og overgang ---
p_turb = P[turbulent_regime, turbulent_regime]
p_rolig = P[rolig_regime, rolig_regime]

dur_turbulent = 1 / (1 - p_turb)
dur_rolig = 1 / (1 - p_rolig)

exit_turbulent = 1 - p_turb
exit_rolig = 1 - p_rolig

# --- Terminalmeldinger ---
print(" ") # (legger luft øverst i terminalen)
print("Skjult Markov Modell – Strukturell regimeanalyse (OSEBX)")
print("(Basert på ukentlig data)\n")  
print("Overgangsmatrise (sannsynlighet for å forbli eller skifte):\n")
print(pd.DataFrame(P, columns=["→Regime0", "→Regime1"], index=["Regime0→", "Regime1→"]))
print("\nForventet varighet (UKER):")  
print(f"• Rolig regime (Regime: {rolig_regime}): {dur_rolig:.2f} uker")
print(f"• Turbulent regime (Regime: {turbulent_regime}): {dur_turbulent:.2f} uker")
print("\nSannsynlighet for regimeskifte:")  
print(f"• Fra rolig → turbulent: {exit_rolig:.4f}")
print(f"• Fra turbulent → rolig: {exit_turbulent:.4f}")
print("\nIdentifiserte regimer basert på gjennomsnittlig volatilitet:")
print(f"• Rolig regime-ID: {rolig_regime}")
print(f"• Turbulent regime-ID: {turbulent_regime}")
print("\nGjennomsnittlig volatilitet pr. regime:")
print(mean_vol_by_state)

# --- Plot: Close-pris og regimer ---
plt.figure(figsize=(12, 6))
plt.plot(df.loc[X_out.index, "rebased_close"], color='black', linewidth=1, label="Markedsbevegelse")

plt.scatter(X_out.index[X_out["Regime"] == turbulent_regime],
            df.loc[X_out.index[X_out["Regime"] == turbulent_regime], "rebased_close"],
            color='red', s=10, label=f"Regime {turbulent_regime} (turbulent)")

plt.scatter(X_out.index[X_out["Regime"] == rolig_regime],
            df.loc[X_out.index[X_out["Regime"] == rolig_regime], "rebased_close"],
            color='green', s=10, label=f"Regime {rolig_regime} (rolig)")

plt.title("OSEBX med HMM-regimer (ukentlig data)") 
plt.xlabel("Dato")
plt.ylabel("Standardisert Close-kurs")
plt.legend()
plt.tight_layout()
plt.show()