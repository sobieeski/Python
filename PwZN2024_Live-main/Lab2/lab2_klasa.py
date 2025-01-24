import numpy as np
import matplotlib.pyplot as plt
from rich.progress import Progress
from PIL import Image, ImageSequence
import os
class IsingModel:
    def __init__(self, rozmiar_siatki, J, beta, B, ilosc_krokow, gestosc_spinow=0.5, img_prefix=None, animacja_plik="animation.gif", magnetization_file=None, outputDirectory = "lab2/wyniki/"):
        os.makedirs(outputDirectory, exist_ok=True)
        self.rozmiar_siatki = rozmiar_siatki
        self.J = J
        self.beta = beta
        self.B = B
        self.ilosc_krokow = ilosc_krokow
        self.gestosc_spinow = gestosc_spinow
        self.img_prefix = img_prefix
        self.animacja_plik = animacja_plik
        self.magnetization_file = magnetization_file
        self.outputDirectory = outputDirectory
        #generoawnie loswej siatki z losowami spinami
        self.spins = np.random.choice([-1, 1], size=(rozmiar_siatki, rozmiar_siatki), p=[1 - gestosc_spinow, gestosc_spinow])
        self.magnetyzacja = []
        self.obrazy = []
    #określa zmiane energii w sasiedztwie 
    def zamiana_energii(self, i, j):
        spin = self.spins[i, j]
        neighbors = (
            self.spins[(i - 1) % self.rozmiar_siatki, j] +
            self.spins[(i + 1) % self.rozmiar_siatki, j] +
            self.spins[i, (j - 1) % self.rozmiar_siatki] +
            self.spins[i, (j + 1) % self.rozmiar_siatki]
        )
        delta_E = 2 * spin * (self.J * neighbors + self.B)
        return delta_E
    
    #mote carlo argument zwraca zmieniona siatkę w zależności od zmian ułożenia spinów
    def monte_carlo_step(self):
        
        for _ in range(self.rozmiar_siatki * self.rozmiar_siatki):
            i, j = np.random.randint(0, self.rozmiar_siatki, size=2)
            delta_E = self.zamiana_energii(i, j)

             #dE jest różnicą energii między stanem początkowym a stanem końcowym.
            if delta_E <= 0 or np.random.rand() < np.exp(-self.beta * delta_E):
                self.spins[i, j] *= -1

    # zapisywanie obrazów siatki do wybranego foldera
    def zapis_zdjec(self, krok):
         if self.img_prefix:
            plt.imshow(self.spins)
            plt.savefig(os.path.join(self.outputDirectory,f"{self.img_prefix}_{krok}.png"), bbox_inches='tight')
            plt.close()

            #Tworzenia tablicy obrazów; tablica ta jest używyna tworzenia gifa 
            img = Image.open(os.path.join(self.outputDirectory,f"{self.img_prefix}_{krok}.png"))
            self.obrazy.append(img)
    #stworzenie gifu
    def zapis_animacji(self):
        if self.animacja_plik and self.obrazy:
            self.obrazy[0].save(
                os.path.join(self.outputDirectory,self.animacja_plik),
                save_all=True,
                append_images=self.obrazy[1:],
                duration=200,
                loop=0
            )
    #zapisanie magnetyzacji do pliku
    def zapis_mnagnetyzacji(self):
        np.savetxt(os.path.join(self.outputDirectory,self.magnetization_file), self.magnetyzacja, header="Wyniki symulacji")
    #wywałanie funkcji 
    def run(self):
       
        with Progress() as progress:
            task = progress.add_task("Trwa symulacja", total=self.ilosc_krokow)

            for step in range(self.ilosc_krokow):
                self.monte_carlo_step()
                mag = np.sum(self.spins) / (self.rozmiar_siatki ** 2)
                self.magnetyzacja.append([step, mag])
                self.zapis_zdjec(step)
                progress.update(task, advance=1)

            self.zapis_animacji()
            self.zapis_mnagnetyzacji()


if __name__ == "__main__":
    model = IsingModel(
        rozmiar_siatki=50, J=1, beta=0.5, B=0, ilosc_krokow=100,
        img_prefix="klatka_nr",
        magnetization_file="magnetyzacja.txt"
    )
    model.run()
