# -- del a --
data = {
    "Norge": ["Oslo", 0.634],
    "England": ["London", 8.982],
    "Frankrike": ["Paris", 2.161],
    "Italia": ["Roma", 2.873]
}

# -- del b --
land = input("Velg et land ")  # Spør om å velge et land i terminalen

if land in data:
    hovedstad = data[land][0]  # Henter ut hovedstaden til landet
    befolkning = data[land][1]  # Henter ut befolkningen til landet
    print(f"{hovedstad} er hovedstaden i {land} og der er {befolkning} mill. innbyggere i {hovedstad}.")  # Skriver ut hovedstaden og befolkningen i terminalen

# -- del c --
else:
    svar = input("Landet er ikke i databasen. Vil du legge det til? ja/nei ").strip().lower()  # Spør om man vil legge til landet i terminalen
    if svar in ("ja", "j", "yes", "y"):
        while True:
            nytt_land = input("Skriv inn et nytt land eller stopp for å avslutte: ").lower().strip() # Spør om et nytt land i terminalen
            
            if nytt_land.lower().strip() == "stopp":
                break
    
            hovedstad = input("Hva er den nye hovedstaden? ")  # Spør om den nye hovedstaden i terminalen
            befolkning = float(input("Hva er den nye befolkningen i millioner? "))  # Spør om den nye befolkningen i terminalen

            data[nytt_land] = [hovedstad, befolkning]  # Legger til landet i databasen
            print(f'{land} med hovedstaden {hovedstad} og befolkningen {befolkning} millioner er lagt til i databasen.')  # Skriver ut at landet er lagt til i terminalen
    
        print(data)  # Skriver ut den oppdaterte databasen i terminalen/skjermen 
    else:
        print("Ok, ingen endringer er gjort")
