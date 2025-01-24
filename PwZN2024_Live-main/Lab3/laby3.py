import numpy as np
import time
from functools import wraps

#Dekorator mierzący czas wykonania funkcji
def czas_wykonania(funkcja):
    statystyki = {"liczba_wykonan": 0, "suma_czasow": 0.0, "min": float('inf'), "max": 0, "odchylenie_stnrdowe" : 0}
    @wraps(funkcja)
    def wrapper():

        start = time.time()
        wynik = funkcja()
        koniec = time.time()
        czas = koniec - start
        print(f"Czas wykonania: {czas:.5f} sekund")
        statystyki["liczba_wykonan"] += 1
        statystyki["suma_czasow"] += czas
        if  statystyki["min"] > czas:
            statystyki["min"] = czas
        if statystyki["max"] < czas:
            statystyki["max"] = czas
        return wynik
       # Dodanie funkcji do odczytu statystyk
    def pobierz_statystyki():
        liczba_wykonan = statystyki["liczba_wykonan"]
        srednia_czasow = statystyki["suma_czasow"] / liczba_wykonan if liczba_wykonan > 0 else 0
        min = statystyki["min"]
        max = statystyki["max"]
        return {
            "liczba_wykonan": liczba_wykonan,
            "srednia_czasow": srednia_czasow,
            "min": min,
            "max": max,
           # "odchylenie_stnrdowe": odchylenie_stnrdowe,
            "srednia_czasow": srednia_czasow,
        }

    wrapper.pobierz_statystyki = pobierz_statystyki
    return wrapper

#Funkcja tworząca tablicę 10000000-elementową z losowymi liczbami od 1 do 100000
@czas_wykonania
def generuj_tablice():
    np.random.randint(1, 100000, 10000000)

#Przykład użycia
generuj_tablice()
generuj_tablice()
generuj_tablice()
generuj_tablice()
generuj_tablice()
generuj_tablice()
generuj_tablice()
generuj_tablice()
generuj_tablice()
statystyki = generuj_tablice.pobierz_statystyki()
print(f"Liczba wykonanych wywołań: {statystyki['liczba_wykonan']}")
print(f"Średni czas wykonania: {statystyki['srednia_czasow']:.5f} sekund")
print(f"Min czas wykonania: {statystyki['min']:.5f} sekund")
print(f"Max czas wykonania: {statystyki['max']:.5f} sekund")

