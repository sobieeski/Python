import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

def fetch_image(url, output_folder):
    """Pobiera obraz z podanego URL i zapisuje go w folderze."""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            filename = os.path.basename(url)
            filepath = os.path.join(output_folder, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Zapisano: {filename}")
    except Exception as e:
        print(f"Błąd pobierania {url}: {e}")

def pobieranie_obrazow_z_podstrony(page_url, output_folder):
    """Pobiera wszystkie obrazy z jednej podstrony."""
    try:
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            image_tags = soup.find_all('img')
            image_urls = [urljoin(page_url, img['src']) for img in image_tags if 'src' in img.attrs]
            for image_url in image_urls:
                fetch_image(image_url, output_folder)
        else:
            print(f"Błąd pobierania strony {page_url}: {response.status_code}")
    except Exception as e:
        print(f"Błąd przetwarzania {page_url}: {e}")

def linki_podstron(base_url):
    """Zwraca listę linków do wszystkich podstron na stronie głównej."""
    links = []
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                full_url = urljoin(base_url, a_tag['href'])
                if base_url in full_url and full_url not in links:
                    links.append(full_url)
        else:
            print(f"Błąd pobierania strony głównej: {response.status_code}")
    except Exception as e:
        print(f"Błąd przetwarzania strony głównej: {e}")
    return links

def main():
    base_url = "https://www.fizyka.pw.edu.pl/Aktualnosci"
    output_folder = "zdjecia"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    page_links = linki_podstron(base_url)
    print(f"Znaleziono {len(page_links)} podstron.")

    with ThreadPoolExecutor() as executor:
        for page_url in page_links:
            executor.submit(pobieranie_obrazow_z_podstrony, page_url, output_folder)

if __name__ == "__main__":
    main()
