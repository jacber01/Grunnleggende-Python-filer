import numpy as np

v_grad = float(input("Skriv inn gradtallet"))  # Spør om gradtall i terminal

v_rad = v_grad * (np.pi / 180)  # Regner om gradtall til radianer

print("Gradtallet i radianer er", v_rad)  # Skriver ut radianer i terminal
