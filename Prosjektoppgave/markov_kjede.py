import warnings
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from hmmlearn.hmm import GaussianHMM
import matplotlib.pyplot as plt

# --- Fjerner støy fra terminalen---
warnings.filterwarnings("ignore")

# --- Konfig ---
show_plot = True  # om Grafen skal vises

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
    n_components=2, # to skjulte tilstander (regimer)
    covariance_type="full", # full kovariansmatrise
    n_iter=500, # maks antall iterasjoner under trening
    random_state=42 # fast tilfeldig startpunkt for reproduserbarhet.
)

model.fit(X_scaled)

# --- Fast overgangsmatrise ---
P = model.transmat_

# --- Predikerer skjulte tilstander ---
states = model.predict(X_scaled)
X_out = X_df.copy()
X_out["State"] = states

# --- Beregner gjennomsnittlig volatilitet og avkastning for å identifisere tilstander ---
mean_vol_by_state = X_out.groupby("State")["realized_volatility_30d"].mean()
mean_ret_by_state = X_out.groupby("State")["log_return"].mean()

volatile_state = mean_vol_by_state.idxmax()
calm_state = mean_vol_by_state.idxmin()

# --- Egendefinert funksjon for å oppfylle oppgavekrav---
def expected_duration(p_stay):  # Returnerer forventet varighet gitt sannsynlighet for å forbli i samme regime.
    return 1 / (1 - p_stay)

# --- Identifiserte regimer for varighet og overgang ---
p_volatile = P[volatile_state, volatile_state]
p_calm = P[calm_state, calm_state] 

dur_volatile = expected_duration(p_volatile)
dur_calm = expected_duration(p_calm)

exit_volatile = 1 - p_volatile
exit_calm = 1 - p_calm

# --- Beregner nåværende regime og hvor lenge vi har vært i det ---
current_state = states[-1]  # siste observerte regime
current_streak = 0
for state in reversed(states):
    if state == current_state:
        current_streak += 1
    else:
        break

# --- Graf: Volatilitet og Avkastning ---
if show_plot:
    plt.figure(figsize=(12, 6))
    plt.axhline(0, color="black", linewidth=1)  # horisontal linje ved 0 (0 % avkastning)

    returns = X_out["log_return"]
    volatility = X_out["realized_volatility_30d"]

    volatility = (volatility - volatility.mean()) / volatility.std() * returns.std()  # standardiserer volatiliteten rundt sitt gjennomsnitt og skalerer til samme startverdi som avkastningen

    for i in range(1, len(X_out)):
        x0, x1 = X_out.index[i - 1], X_out.index[i]
        color = "red" if X_out["State"].iloc[i] == volatile_state else "green"
        plt.axvspan(x0, x1, color=color, alpha=0.14, zorder=0)

    plt.plot(X_out.index, returns, color="blue", linewidth=0.6, label="Avkastning")
    plt.plot(X_out.index, volatility, color="orange", linewidth=0.6, label="Volatilitet")
    plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    plt.title("OSEBX Avkastning og Volatilitet over tid")
    plt.xlabel("Dato")
    plt.ylabel("Avkastning (%)")
    ax2 = plt.gca().secondary_yaxis("right", functions=(lambda x: x + X_out["realized_volatility_30d"].mean(), lambda x: x - X_out["realized_volatility_30d"].mean())) # høyre y-akse der 0-linjen samsvarer med gjennomsnittlig volatilitet                                               
    ax2.set_ylabel(f"Volatilitet (30d) – gj.snitt: {X_out['realized_volatility_30d'].mean():.3f}")  # etikett for høyre y-akse
    plt.legend()
    plt.tight_layout()
    plt.show()

# --- Terminalmeldinger ---
print(" ")  # luft i terminalen
print("Skjult Markov Modell – Strukturell regimeeanalyse (OSEBX)")
print("(Basert på ukentlig data)\n")

print("Overgangsmatrise (sannsynlighet for å forbli eller skifte):\n")
print(pd.DataFrame(P, columns=["→ Regime 0", "→ Regime 1"], index=["Regime 0→", "Regime 1→"]))

print("\nForventet varighet pr. regime:")
print(f"• Rolig regime (Regime: {calm_state}): {dur_calm:.2f} uker")
print(f"• Turbulent regime (Regime: {volatile_state}): {dur_volatile:.2f} uker")

print("\nSannsynlighet for regime-skifte:")
print(f"• Fra rolig → turbulent: {exit_calm:.4f}")
print(f"• Fra turbulent → rolig: {exit_volatile:.4f}")

print("\nGjennomsnittlig avkastning pr. regime:")
for state_id, ret in mean_ret_by_state.items():
    print(f"Regime {state_id}: Gjennomsnittlig avkastning = {ret:.4f}")

print("\nGjennomsnittlig volatilitet pr. regime:")
for state_id, vol in mean_vol_by_state.items():
    print(f"Regime {state_id}: Gjennomsnittlig volatilitet = {vol:.4f}")

print("\nNåværende markedsregime:")
print(f"• Identifisert regime: {current_state}")
print(f"• Antall uker i nåværende regime: {current_streak}")
print(" ")  # luft i terminalen 
