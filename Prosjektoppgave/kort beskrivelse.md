## Problemet jeg ønsker å løse
Denne koden er laget med bakgrunn fra mitt masterprogram i finans. Koden skal kunne brukes som et verktøy til å analysere om aksjemarkedet er i en tubulent eller rolig fase (også kalt regime).

## Filene som er i mappen
Mappen består i hovedsak av 4 filer. 
markov_kjede.py er kjernen i prosjektoppgaven, det er denne som kjører maskinlæringsmodellen og printer ut resultatene oppnådd.
data_eksport.py er brukt til å regne-, vaske- og generere datafilen som trengs for å kunne kjøre markov_kjede.py filen.
OSEBX_data.csv er selve dataen jeg brukte på min test av koden, den ble laget av data_eksport i Oktober 2025. Om det er ønskelig kan man kjøre data_eksport.py på nytt og få helt oppdatert data med ferkse resultater.
OSEBX_Ret_Vol.png er plotten som markov_kjede.py lager. Den viser visuelt hvordan markedet har sett ut de siste 3 årene. Den er farget til grønn og rød basert på når koden mente markedet var turbulent eller rolig. Det er også satt opp Avkastning og volatilitet (som er to av de fire variablene modellen bruker) som hjelp til å kunne vise hvordan disse to variablene så ut når markedet var turbulent eller rolig. Det som er interessant her, er at vi ser tydelige svinginger på både avkastningen og volatiliteten når markedet er i rød(turbulent). Som kan tyde på at modellen klarte å klassifisere riktig.

Koden følger oppgave kravene teknisk. 
Skrive data til fil og de vektoriserte beregningene eksisterer i data_eksport.py filen, som regner ut rullerende 30 dagers volatilitet, logaritmiske avkastning, høy-lav spread og z-score for handels volum 
markov_kjede.py inneholder de resterende kravene som if/else-tester, lese data fra fil, plotting osv. 

*AI erklæring: Kunstlig intelligens (AI) er ikke brukt til å generere noe kode i denne oppgaven. AI er kun benyttet som et verktøy for å hjelpe med å forstå og forklare resultatene oppnådd fra koden.*
