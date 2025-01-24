import requests
from bs4 import BeautifulSoup
import json

url = "https://www.f1-fansite.com/pl/Wyniki-f1/mistrzowie-f1/"
res = requests.get(url)


soup = BeautifulSoup(res.text, 'html.parser')
mistrzowie = []

for row in soup.select('table tbody tr'):  # wskaznie miejsca gdzie są interesujące nas dane
  columns = row.find_all(['td', 'th'])  # Uwzględnienie  <td> i <th> bo w th znajduję się rok
  if len(columns) >= 4:  # Sprawdzamy czy są 4 kolumny bo w nich są interesujące nas dane w kolumnie 2 (jeśli liczymy od 0) znajduje się zdjęcie które nas nie interesuje
    rok = columns[0].get_text(strip=True)  # Pobranie roku
    name = columns[1].get_text(strip=True)  # Pobranie imienia i nazwiska
    zespol = columns[3].get_text(strip=True)  # Pobranie zespołu
    mistrzowie.append({"rok": rok, "imie nazwisko": name, "zespol": zespol})
    if rok == "1950": #zabezpiecznie bo pobierane były dane z innych tabel (rok ustanowienia pierwszego mistrza)
        break


#print(mistrzowie)
output_file = "f1_mistrzowie.json"
with open(output_file, 'w', encoding='utf-8') as file:
  json.dump(mistrzowie, file, ensure_ascii=False, indent=4)






