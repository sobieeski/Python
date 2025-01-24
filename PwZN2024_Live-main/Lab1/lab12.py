import re
import os
import argparse
import collections
from collections import Counter
from rich.progress import track
from ascii_graph import Pyasciigraph
from _collections_abc import Iterable
collections.Iterable = Iterable
import matplotlib.pyplot as plt
from ascii_graph import colors


  # Funkcja wczytująca tekst z pliku
def read_text(plik):                                  
    try:
        with open(plik, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Błąd podczas odczytu pliku '{plik}': {e}")
        return ""

# Funkcja dzieląca tekst na pojedyńcze wyrazy i filtrująca je 
def process_text(text, min_dlugosc, ignorowane_slowa, ma_nie_zawierac_znakow, ma_zawierac_znaki):
    # Podział tekstu na słowa
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = []
    for word in words:
        if len(word) < min_dlugosc:
            continue
        if word in ignorowane_slowa:
            continue
        if any(substr in word for substr in ma_nie_zawierac_znakow):
            continue
        if ma_zawierac_znaki and not any(substr in word for substr in ma_zawierac_znaki):
            continue
        filtered_words.append(word)

    return filtered_words

# Funkcja tworzacas liste najczęściej się powtarzających słow wraz z ich z liczeniem  
def lista_slow(slowa, jak_duzy_histogram):
    word_counts = Counter(slowa).most_common(jak_duzy_histogram)
    return word_counts

# Funkcja do wyświetlania histogramu oraz ubrawijąca dany kolor histyogramu w zależności od ilości powtarzjących się wyrazów
def wyswietl_histogram(histogram):
   
    graph = Pyasciigraph()
    data = [(word, count, colors.Gre) for word,count in histogram]
    new_data = []
    for x, y, z in data:
        if y < 10:
            new_data.append((x, y, colors.Red))
        if y > 10 and y < 25 : 
             new_data.append((x, y, z)) 
        if y > 25: 
            new_data.append((x, y, colors.BCya)) 

    for line in graph.graph('Histogram', new_data):
        print(line)
        
        
# Funkcja do obsługi wielu plików w katalogu
def process_directory(directory, min_dlugosc, ignorowane_slowa,  ma_nie_zawierac_znakow, ma_zawierac_znaki, jak_duzy_histogram):
    all_words = []
    for file_name in track(os.listdir(directory), description="Przetwarzanie plików..."):
        plik = os.path.join(directory, file_name)
        if os.path.isfile(plik) and file_name.endswith('.txt'):
            text = read_text(plik)
            words = process_text(text, min_dlugosc, ignorowane_slowa,  ma_nie_zawierac_znakow, ma_zawierac_znaki)
            all_words.extend(words)

    histogram = lista_slow(all_words, jak_duzy_histogram)
    wyswietl_histogram(histogram,jak_duzy_histogram)

# Główna funkcja
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generowanie histogramu słów z pliku tekstowego.")
    parser.add_argument("file", help="Nazwa pliku z jakiego brany będzie tekst")
    parser.add_argument("-n", "--jak_duzy_histogram", type=int, default=10, help="Paramater okreslający wielkość histogramu; domyślna wartość 10")
    parser.add_argument("-l", "--min_dlugosc", type=int, default=0, help="Minimalna długość słowa (domyślnie 0).")
    parser.add_argument("-i", "--ignorowane_slowa", nargs='*', default=[], help="Słowa ignorowane")
    parser.add_argument("-x", "--ma_nie_zawierac_znakow", nargs='*', default=[], help="Ciągi znaków, jakie wyrazy nie mogą mieć")
    parser.add_argument("-c", "--ma_zawierac_znaki", nargs='*', default=[], help="Ciągi znaków, jakie wyrazy muszą mieć")
   

    args = parser.parse_args()

    if os.path.isdir(args.file):
        process_directory(args.file, args.min_dlugosc, args.ignorowane_slowa, args.ma_nie_zawierac_znakow, args.ma_zawierac_znaki, args.jak_duzy_histogram)
    else:
        text = read_text(args.file)
        words = process_text(text, args.min_dlugosc, args.ignorowane_slowa, args.ma_nie_zawierac_znakow, args.ma_zawierac_znaki)
        histogram = lista_slow(words, args.jak_duzy_histogram)
        wyswietl_histogram(histogram)
