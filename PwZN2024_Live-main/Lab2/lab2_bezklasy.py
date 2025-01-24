import numpy as np
import matplotlib.pyplot as plt
import os
from rich.progress import Progress
from PIL import Image, ImageSequence

rozmiar_siatki = 100
B = 0.1 #wartość pola magnetycznego
J = 1
beta = 0.9
ilosc_krokow = 100
gestosc_spinow = 0.5
tablica_OBRAZOW = []
dane = []
animation_file="animation.gif"
outputDirectory = "lab2/wyniki/"
os.makedirs(outputDirectory, exist_ok=True)
print(f"Rozpoczęcie symulacji. Png zaipsują się w: {outputDirectory} losowość: {gestosc_spinow} liczba kroków: {ilosc_krokow} siatka: {rozmiar_siatki}")


#generoawnie loswej siatki z losowami spinami
def fill_np_simulation_grid(rozmiar_siatki, gestosc_spinow):
    symulacja_siatki = np.random.choice([-1, 1], size=(rozmiar_siatki, rozmiar_siatki), p=[gestosc_spinow, 1-gestosc_spinow])
    return symulacja_siatki
#określa zmiane energii w sasiedztwie 
def zmiana_enrgii(symulacja_siatki,i,j):
    siatka = symulacja_siatki[i,j]
    neighbors = (
            symulacja_siatki[(i - 1) % rozmiar_siatki, j] +
            symulacja_siatki[(i + 1) % rozmiar_siatki, j] +
            symulacja_siatki[i, (j - 1) % rozmiar_siatki] +
            symulacja_siatki[i, (j + 1) % rozmiar_siatki]
        )
    delta_E = 2 * siatka * (J * neighbors + B)
    return delta_E
#mote carlo argument zwraca zmieniona siatkę w zależności od zmian ułożenia spinów
def  monte_carlo(symulacja_siatki):
   
    for _ in range(rozmiar_siatki**2):
        i, j = np.random.randint(0,rozmiar_siatki, size=2)
        delta_E = zmiana_enrgii(symulacja_siatki,i, j)
        #dE jest różnicą energii między stanem początkowym a stanem końcowym. 
        if delta_E <= 0 or np.random.rand() < np.exp(-beta * delta_E):
            symulacja_siatki[i, j] *= -1
    return symulacja_siatki
# zapisywanie obrazów siatki do wybranego foldera
def save_image(symulacja_siatki, outputDirectory, iteration):
    plt.imshow(symulacja_siatki)
    plt.savefig(os.path.join(outputDirectory, f"obraz{iteration}.png"))
    plt.close()
#funckja do tworzenia tablicy obrazów,. tablica ta jest używyna tworzenia gifa   
def pomoc_do_gifa( outputDirectory, iteration):
    img = Image.open(os.path.join(outputDirectory,f"obraz{iteration}.png"))
    tablica_OBRAZOW.append(img)
    return tablica_OBRAZOW
#zapisanie magnetyzacji do pliku
def zapis_mnagnetyzacji():
   np.savetxt(os.path.join(outputDirectory,f"magnetyzacja.text"),dane)
#stworzenie gifu
def save_animation():
    if animation_file and tablica_OBRAZOW:
        tablica_OBRAZOW[0].save(
            os.path.join(outputDirectory,animation_file),
            save_all=True,
            append_images=tablica_OBRAZOW[1:],
            duration=200,
            loop=0
        )
#main w którym wywoływane są funckje    
if __name__ == "__main__":
    symulacja_siatki = fill_np_simulation_grid(rozmiar_siatki, gestosc_spinow)
  
    with Progress() as progress:
        task = progress.add_task("Running simulation...", total = ilosc_krokow)  #tworzenie pasku postępu 
        for k in range(ilosc_krokow):
            symulacja_siatki = monte_carlo(symulacja_siatki)
            save_image(symulacja_siatki, outputDirectory, k)
            pomoc_do_gifa( outputDirectory, k)
            mag = np.sum(symulacja_siatki) / (rozmiar_siatki ** 2) #obliczanie magnetyzacji
            dane.append([k, mag])
            progress.update(task, advance=1)
    save_animation()
    zapis_mnagnetyzacji()