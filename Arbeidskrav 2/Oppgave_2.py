import math

antall_elever = int(input("Hvor mange elever er det i klassen? ")) # Spør om antall elever i terminal

pizza_per_elev = 0.25 # Hver elev spiser 1/4 pizza

total_pizza = antall_elever * pizza_per_elev # Regner ut totalt antall pizza

kjøpe_pizza = math.ceil(total_pizza) # Runder opp til nærmeste hele pizza som skal kjøpes

print("Du må kjøpe", kjøpe_pizza, "pizzaer.") # Skriver ut antall pizza som må kjøpes i terminal
