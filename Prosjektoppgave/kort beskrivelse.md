## Problemet jeg ønsker å løse
Denne koden er laget med bakgrunn fra mitt masterprogram i finans. Koden skal brukes som et verktøy for å analysere om aksjemarkedet er i en turbulent eller rolig fase (også kalt regime).

## Filene som er i mappen
Mappen består i hovedsak av fire filer.

markov_kjede.py er kjernen i prosjektoppgaven; det er denne som kjører maskinlæringsmodellen og skriver ut resultatene som oppnås.

data_eksport.py brukes til å beregne, vaske og generere datafilen som trengs for å kjøre markov_kjede.py.

OSEBX_data.csv er selve datasettet som ble brukt til testing av koden. Det ble generert av data_eksport.py i oktober 2025. Ved behov kan man kjøre data_eksport.py på nytt for å hente oppdaterte data med ferske resultater.

OSEBX_Ret_Vol.png er plottet som markov_kjede.py genererer. Det viser visuelt hvordan markedet har utviklet seg de siste tre årene.

Plottet er farget grønt og rødt basert på når koden vurderer markedet som henholdsvis rolig eller turbulent. I tillegg vises avkastning og volatilitet (to av de fire variablene modellen bruker) for å illustrere hvordan disse utvikler seg i de ulike regimene.

Det som er interessant her, er at det fremkommer tydelige svingninger i både avkastning og volatilitet når markedet er i den røde (turbulente) fasen. Dette kan indikere at modellen har klassifisert tilstandene korrekt.

### Koden følger oppgave kravene teknisk. 
Skriving av data til fil og vektoriserte beregninger er implementert i data_eksport.py, som beregner rullerende 30-dagers volatilitet, logaritmisk avkastning, høy-lav-spread og z-score for handelsvolum.

markov_kjede.py inneholder de resterende kravene, som if/else-tester, while løkker, innlesing av data fra fil, plotting osv.

*For en dypere analyse og forklaring av koden, les Grundig beskrivelse.md

## AI erklæring

*Kunstlig intelligens (AI) er ikke brukt til å generere noe kode i denne oppgaven. AI er kun benyttet som et verktøy for å hjelpe med å forstå og forklare resultatene oppnådd fra koden.*
