import numpy as np
import matplotlib.pyplot as plt

# Parametry początkowe
S0 = 0.98  # Początkowa liczba podatnych na zakażenie
I0 = 0.02  # Początkowa liczba zakażonych
R0 = 0.0   # Początkowa liczba ozdrowieńców
parametry_poczatkowe = (S0, I0, R0)

beta = 0.5  # Współczynnik zakaźności
gamma = 0.01  # Współczynnik ozdrowień

T = 200  # Liczba kroków czasowych
dt = 0.1  # Długość kroku czasowego

krok_czasowy = int(T / dt)

# Funkcja opisująca model SIR
def sir_model(y, beta, gamma):
    S, I, R = y
    return np.array([-beta * S * I,beta * S * I - gamma * I, gamma * I])

# Funkcja do rozwiązywania układu równań różniczkowych metodą Eulera
def rozwiaznie_sir(parametry_poczatkowe, beta, gamma, time_steps):
    S, I, R = parametry_poczatkowe
    results = np.zeros((time_steps, 3))  # Przechowujemy S, I, R
    results[0] = [S, I, R]

    for t in range(1, time_steps):
        results[t] = results[t - 1] + sir_model(results[t - 1], beta, gamma) * dt

    return results


# Rozwiązywanie układu
results = rozwiaznie_sir(parametry_poczatkowe, beta, gamma, krok_czasowy)
czas = np.linspace(0, T, krok_czasowy)

# Wizualizacja wyników
plt.figure(figsize=(10, 10))
plt.plot(czas, results[:, 0], label='Podatni (S)')
plt.plot(czas, results[:, 1], label='Zakażeni (I)')
plt.plot(czas, results[:, 2], label='Ozdrowieńcy (R)')

plt.title('Model SIR')
plt.xlabel('Czas')
plt.ylabel('Udział populacji')
plt.legend()
plt.grid()
plt.show()
