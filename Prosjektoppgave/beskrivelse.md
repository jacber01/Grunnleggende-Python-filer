# Regimeidentifikasjon på Oslo Børs med Skjult Markov-modell (HMM)

Dette prosjektet bruker en **Skjult Markov-Modell** til å identifisere underliggende markedsregimer på Oslo Børs. Modellen analyserer historiske data og avdekker skjulte regimer som kan brukes til risikostyring og porteføljetilpasning.

## Prosjektmål

Koden kan brukes til å svare på spørsmålet: *Hvor eksponert bør en invenstor være i Oslo Børs akkurat nå? *

Modellen:
- Henter og analyserer data fra OSEBX-indexen f.o.m 3 år siden t.o.m seneste handelsdag
- Identifiserer automatisk to distinkte markedsregimer basert på 4 forskjellige variabler (Volum, Volatilitet, Avkastning og Intradag spedning)
- Gir probabilistiske prediksjoner om fremtidige regimeskift

---

## Hva er en Markov-modell?

### Intuitivt eksempel

La oss si at en restaurant har et daglig lunsjtilbud som består av **enten** Pizza, Burger eller Taco. Og at du ønsker å finne mønsteret mellom disse tre tilbudene (også kalt "regimene"). Hovedantakalsen i en Markov modell er at sannsynligheten for hva morgendagens lunsjtilbud blir, er kun avhengig av hva lunsjtilbudet var i dag. Dette uttrykkes mattematisk som:

$P(X_{t+1} \mid X_t)$

Etter å ha observert restauranten over tid kan vi konstruere en overgangsmatrise som beskriver sannsynlighetene for hvert neste steg:

|                     | → Burger (i morgen) | → Pizza (i morgen) | → Taco (i morgen) |
|---------------------|---------------------|--------------------|---------------------|
| **Fra Burger (i dag)** | 20%                 | 50%                | 30%                 |
| **Fra Pizza (i dag)**  | 60%                 | 10%                | 30%                 |
| **Fra Taco (i dag)** | 40%                 | 40%                | 20%                 |

### Hvordan modellen faktisk “ser” bevegelsene

En vanlig misforståelse er at Markov-modellen “følger regimene” fra sted til sted i sanntid. Det gjør den ikke. Modellen ser kun tilstandende som punktvise observasjoner over tid.  
Med andre ord: den ser at det var Pizza i dag, og bruker kun det for å estimere sannsynligheten for hva lunsjtilbudet blir neste gang én av disse definerte regimene oppnås. Den bryr seg ikke om eventuelle mellomstopp, eller i dette tilfelle, andre tilbud underveis.

Hver dag er altså ett *tidssteg* der Restauranten befinner seg i én av tre mulige tilstander. Neste dag velges en ny tilstand basert på overgangssannsynlighetene i tabellen over.  
Dette kalles en **diskret Markov-prosess**.

---

### Prediksjonsmekanikk: Hvordan bruker vi dette?

**Scenario:** I dag er Restauranten i regime: **Pizza**.  
Da representeres dagens tilstandsvektor slik:

$\pi_t = [P(\text{Burger})=0, P(\text{Pizza})=1, P(\text{Taco})=0]$

Overgangsmatrisen $P$  definerer hvordan du kan gå til neste dag:

Fra Pizza → Burger: 60%  
Fra Pizza → Pizza: 10%  
Fra Pizza → Taco: 30%

Matematisk:

$\pi_{t+1} = \pi_t \cdot P$

Resultatet blir:
$\pi_{t+1} = [0.60,\ 0.10,\ 0.30]$

Dette betyr at hvis Restaurant hadde Pizza i dag, er det 60 % sjanse for at det blir burger i morgen, 10 % for Pizza igjen, og 30 % for Taco.

---

### Anvendelse på aksjemarkedet

I den finansielle verden vil “tilstandene” i min modell oversettes til markedsregimer:
- **Regime 0**
- **Regime 1** 

Der regime med lavest gjennomsnittsvolatilitet klassifiseres som "rolig" og den med høyest volatilitet klassifiseres som "turbulent"

En vanlig Markov-modell antar at vi kan observere regimet direkte. Vi kan da beregne sannsynligheten for overgang fra ett regime til et annet basert på observasjoner av dagens regime.

**Problemet:** I virkeligheten vet vi ikke hvilket regime markedet er i. Vi kan kun observere handlinger som er påvirket av tilstanden (er volatiliteten stor, er volumet stort osv.). Regimene er nemlig skjulte. Dette løses med en skjult Markov-modell.

---

## Hva er en skjult Markov-modell (HMM)?

### Intuitivt eksempel

Du prøver å finne ut om vennen din har en god dag eller dårlig dag, men du kan ikke spørre direkte. I stedet observerer du:
- Snakker mye/lite  
- Smiler/ikke smiler  
- Spiser normalt/hopper over måltider  

Du kan ikke observere den “skjulte” tilstanden (god/dårlig dag), men du kan se symptomene.  
Ved å observere mange dager lærer modellen sammenhengen mellom skjulte tilstander og observerte signaler.

---

### To lag i en HMM

1. **Skjulte tilstander** – det vi ikke ser direkte (markedsregimer, humør,)  
2. **Observerbare signaler** – det vi faktisk måler (avkastning, volum, volatilitet, atferd)

Modellen lærer tre typer sannsynligheter:
1. **Start-sannsynligheter** – hvor vi trolig starter  
2. **Overgangssannsynligheter** – hvordan vi flytter mellom tilstander  
3. **Emisjons-sannsynligheter** – hvor sannsynlig en observasjon er gitt en tilstand  

Den identifiserer tilstander som “Regime 0” og “Regime 1”, uten å vite hva de betyr. Analytikeren må tolke dem ved å se på dataene:
- Gjennomsnittlig volatilitet i hver tilstand  
- Gjennomsnittlig avkastning  
- Hvilke perioder i historien de sammenfaller med  

---

### Anvendelse i finansmarkedet

**Skjulte tilstander:** To markedsregimer (rolig vs turbulent)  
**Observerbare signaler:** Avkastning, volatilitet, volum, HL spread  

**Hvordan det fungerer:**
1. Vi observerer dagens markedsdata (f.eks. −2 % avkastning, høy volatilitet, høyt volum).  
2. Modellen bruker noe som heter **Baum–Welch-algoritmen** til å estimere hvilke regimer som best forklarer observasjonene.  
3. Den gir deretter sannsynligheten for at vi befinner oss i hvert regime akkurat nå.

**Eksempeloutput:**
> “Basert på dagens data er det 87 % sannsynlig at markedet forblir i Regime 1.”

Vi tolker deretter hva Regime 1 betyr, gjennom å se om gjennomsnittsvolatiliteten er høyere eller lavere enn regime 0.

---

### Algoritmer (forenklet)

- **Viterbi-algoritmen**: finner den mest sannsynlige sekvensen av skjulte tilstander over tid.  
- **Forward–Backward-algoritmen**: beregner sannsynligheten for hver tilstand på hvert tidspunkt.  
- **Baum–Welch-algoritmen**: justerer modellparametrene iterativt slik at modellen best passer observasjonene (variant av EM-algoritmen).

---

## Praktisk anvendelse: Risikostyring

Etter at modellen er trent og regimene tolket, kan vi bruke den slik:
- **Redusere leverage** i volatile regimer  
- **Øke eksponering** i stabile regimer  
- **Justere porteføljen proaktivt** ved høy sannsynlighet for regimeskift  

**Eksempel:**
- Modellen sier “87 % sjanse for Regime 1”
- Vi vet Regime 1 historisk tilsvarer høy volatilitet og lav avkastning  
- **Tiltak:** Reduser aksjeeksponering fra 100 % til 60 %, øk kontantandel, sett tettere stop-loss  

---

## Resultater

### Identifiserte regimer 

**Regime 0:**
- Gjennomsnittlig volatilitet: [19%]  
- Klassifikasjon: Turbulent markedsregime  
- Gjennomsnittlig varighet: [7] uker  
- Historiske hendelser der regime 0 ble observert: [Silicon Valley Bank og Credit Suisse-kollapsene (Apr.2023), Oljeprisen korrigerte kraftig ned fra sommerens høyder i Sept. 2024, Trump-tariffkrisen og handelskrig mellom USA og Kina (Apr. 2025)]

**Regime 1:**
- Gjennomsnittlig volatilitet: [11%]  
- Klassifikasjon: Rolig markedsregime 
- Gjennomsnittlig varighet: [42] uker  
- Historiske hendelser der regime 1 ble observert: [Perioder med jevn oppgang og lav volatilitet, typisk juni 2023 til sommer 2024]

**Overgangssannsynligheter:**

|               | → Regime 0 | → Regime 1 |
|---------------|------------|------------|
| **Fra Regime 0** | [85.8]% | [14.2]% |
| **Fra Regime 1** | [2.3]% | [97.7]% |

---

## August 2025: Nåværende tilstand

- **Identifisert regime:** Regime 1  (rolig)
- **Varighet:** ~43 uker på gjennomsnitt 
- **Overgangssannsynlighet:** 2.3% sjanse at vi går over til et turbulent regime  
- **Anbefaling:** Basert på modellen kan en investor vurdere å fortsette å holde en betydelig andel aktiva i porteføljen sin, framfor risikofritt alternativ. Vi er i et rolig regime med sterk sannsynlighet for å bli her i de nærmeste ukene framover.  

---

## Konklusjon

**Styrker:**
- Objektiv regimeidentifikasjon via Baum–Welch  
- Probabilistisk rammeverk (ikke binære svar)  
- Multivariat robusthet (flere datakilder)  
- Kan varsle regimeskift tidlig  

**Begrensninger:**
- Antall regimer må defineres på forhånd  
- Markov-egenskapen kan være for enkel  
- Krever periodisk re-estimering  

**Mulige utvidelser:**
- Flere enn to regimer  
- Inkludere makrovariabler (renter, oljepris, inflasjon)  
- Rullerende online-trening  
- Backtesting av regime-baserte strategier  

---

### Variabler brukt i modellen

#### 1. Close Price (sluttkurs)
- Beregner log-avkastning  
- Indikerer trend og momentum  

#### 2. Daglig avkastning
$r_t = \ln\left(\frac{Close_t}{Close_{t-1}}\right)$
- Fanger retning og endringstakt  
- Brukes som hovedsignal i regimeanalyse  

#### 3. Volum (handelsvolum)
- Måler markedsaktivitet  
- Normaliseres via z-score  

#### 4. Realized Volatility (30 dager)
$\sigma_{30d} = \text{std}(r_{t-30:t}) \times \sqrt{252}$
- Hovedindikator for markedsrisiko  

#### 5. High–Low Spread
$HL\_Spread = \frac{High - Low}{Close}$
- Fanger intradag-usikkerhet  

---

## Bruk
1. `pip install numpy pandas yfinance hmmlearn matplotlib seaborn scikit-learn`  
2. Kjør `data_export.py` for å exportere og regne ut OSEBX-data  
3. Kjør `markov_kjede.py` for å kjøre modellen 
---

*Prosjektoppgave i PY1010, Universitetet i Sørøst-Norge*