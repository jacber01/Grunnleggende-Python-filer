import math

a = float(input("side a: "))  
b = float(input("side b: "))  

c = (a**2 + b**2)**0.5  # regner ut hypotenusen gjennom pytagoras

r = a / 2  # radius til halvsirkelen

areal_sirkel = (math.pi * r**2) / 2  # deler på to fordi figuren i oppgaven er en halvsirkel
omkrets_sirkel = math.pi * r  # regner ut omkretsen til halve sirkelen (2πr / 2 = πr) 

areal_trekant = (a * b) / 2  

areal_total = areal_sirkel + areal_trekant  # regner ut total areal ved å legge sammen arealet til trekanten og halvsirkelen
omkrets_total = omkrets_sirkel + b + c  # regner ut total omkrets ved å legge sammen omkretsen til halvsirkelen og de to sidene

print(f"Arealet til figuren er {round(areal_total, 2)}")  # runder arealet til to desimaler
print(f"Omkretsen til figuren er {round(omkrets_total, 2)}") # runder omkretsen til to desimaler
