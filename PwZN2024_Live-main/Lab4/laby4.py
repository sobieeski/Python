import numpy as np
import matplotlib.pyplot as plt
import os
from rich.progress import Progress
from PIL import Image
from numba import njit
import time

rozmiar_siatki = 100
B = 0.1  # wartość pola magnetycznego
J = 1
beta = 0.9
ilosc_krokow = 100
gestosc_spinow = 0.5
tablica_OBRAZOW = []
dane = []
animation_file = "animation.gif"
outputDirectory = "lab4/wyniki/"
os.makedirs(outputDirectory, exist_ok=True)
print(f"Rozpoczęcie symulacji. Png zapiszą się w: {outputDirectory} losowość: {gestosc_spinow} liczba kroków: {ilosc_krokow} siatka: {rozmiar_siatki}")

# Generowanie losowej siatki z losowymi spinami
def fill_np_simulation_grid(rozmiar_siatki, gestosc_spinow):
    symulacja_siatki = np.random.choice([-1, 1], size=(rozmiar_siatki, rozmiar_siatki), p=[gestosc_spinow, 1-gestosc_spinow])
    return symulacja_siatki

# Określa zmianę energii w sąsiedztwie
@njit
def zmiana_enrgii(symulacja_siatki, i, j, rozmiar_siatki, J, B):
    siatka = symulacja_siatki[i, j]
    neighbors = (
        symulacja_siatki[(i - 1) % rozmiar_siatki, j] +
        symulacja_siatki[(i + 1) % rozmiar_siatki, j] +
        symulacja_siatki[i, (j - 1) % rozmiar_siatki] +
        symulacja_siatki[i, (j + 1) % rozmiar_siatki]
    )
    delta_E = 2 * siatka * (J * neighbors + B)
    return delta_E

# Monte Carlo, argument zwraca zmienioną siatkę w zależności od zmian ułożenia spinów
@njit
def monte_carlo(symulacja_siatki, rozmiar_siatki, J, B, beta):
    for _ in range(rozmiar_siatki**2):
        i, j = np.random.randint(0, rozmiar_siatki, size=2)
        delta_E = zmiana_enrgii(symulacja_siatki, i, j, rozmiar_siatki, J, B)
        if delta_E <= 0 or np.random.rand() < np.exp(-beta * delta_E):
            symulacja_siatki[i, j] *= -1
    return symulacja_siatki

# Zapisywanie obrazów siatki do wybranego folderu
def save_image(symulacja_siatki, outputDirectory, iteration):
    plt.imshow(symulacja_siatki, cmap='coolwarm')
    plt.axis('off')
    plt.savefig(os.path.join(outputDirectory, f"obraz{iteration}.png"))
    plt.close()

# Funkcja do tworzenia tablicy obrazów, używana do tworzenia GIF-a
def pomoc_do_gifa(outputDirectory, iteration):
    img = Image.open(os.path.join(outputDirectory, f"obraz{iteration}.png"))
    tablica_OBRAZOW.append(img)
    return tablica_OBRAZOW

# Zapisanie magnetyzacji do pliku
def zapis_magnetyzacji():
    np.savetxt(os.path.join(outputDirectory, "magnetyzacja.txt"), dane)

# Stworzenie GIF-a
def save_animation():
    if animation_file and tablica_OBRAZOW:
        tablica_OBRAZOW[0].save(
            os.path.join(outputDirectory, animation_file),
            save_all=True,
            append_images=tablica_OBRAZOW[1:],
            duration=200,
            loop=0
        )

# Main, w którym wywoływane są funkcje
if __name__ == "__main__":
    start_time = time.time()
    symulacja_siatki = fill_np_simulation_grid(rozmiar_siatki, gestosc_spinow)

    with Progress() as progress:
        task = progress.add_task("Trwa symulacja....", total=ilosc_krokow)  # Tworzenie paska postępu
        for k in range(ilosc_krokow):
            symulacja_siatki = monte_carlo(symulacja_siatki, rozmiar_siatki, J, B, beta)
            save_image(symulacja_siatki, outputDirectory, k)
            pomoc_do_gifa(outputDirectory, k)
            mag = np.sum(symulacja_siatki) / (rozmiar_siatki ** 2)  # Obliczanie magnetyzacji
            dane.append([k, mag])
            progress.update(task, advance=1)
    end_time = time.time()
    save_animation()
    zapis_magnetyzacji()
   
    print(f"Czas wykonania : {end_time - start_time:.3f} s")