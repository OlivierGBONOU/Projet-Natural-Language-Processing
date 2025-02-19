import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import pandas as pd
import random
from bs4 import BeautifulSoup

# A changer
artist = "Charles Aznavour"
website = "https://paroles2chansons.lemonde.fr/paroles-charles-aznavour?page="
nb_pages = 15

async def get_song_links(driver, song_selector, title_selector, link_selector):
    """Récupère tous les liens et titres des chansons sur une page"""
    songs_info = []
    song_divs = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, song_selector))
    )
    
    for div in song_divs:
        try:
            title = div.find_element(By.CSS_SELECTOR, title_selector).text.strip()
            link = div.find_element(By.CSS_SELECTOR, link_selector).get_attribute("href")
            songs_info.append({"title": title, "url": link})
        except (NoSuchElementException, StaleElementReferenceException) as e:
            print(f"Erreur lors de l'extraction du lien: {e}")
            continue
    
    return songs_info

async def get_lyrics(session, url):
    """Récupère les paroles d'une chanson"""
    try:
        async with session.get(url, ssl=False) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            lyrics_elements = soup.select("p.text-center div")
            lyrics = ' '.join([elem.text.strip() for elem in lyrics_elements if elem.text.strip()])
            lyrics = lyrics.replace("\n", " ")
            lyrics = ' '.join(lyrics.split())
            return lyrics
    except Exception as e:
        print(f"Erreur lors de l'extraction des paroles: {e}")
        return ""

async def main():
    songs = []
    driver = None
    
    try:
        # Configurer les options du navigateur
        edge_options = Options()
        edge_options.add_argument("--headless")  # S'exécute sans ouvrir le navigateur
        edge_options.add_argument(f"--remote-debugging-port={random.randint(9000, 9999)}")
        
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        
        # Sélecteurs CSS
        song_selector = "[class*='flex flex-row items-center gap-2 py-2']"
        title_selector = "a.text-gray-700"
        link_selector = "a[href]"
        
        async with aiohttp.ClientSession() as session:
            # Parcourir toutes les pages
            for page in range(1, nb_pages + 1):
                print(f"Traitement de la page {page}")
                driver.get(website + str(page))
                
                # Récupérer tous les liens des chansons sur la page
                page_songs = await get_song_links(driver, song_selector, title_selector, link_selector)
                
                # Pour chaque chanson, récupérer les paroles
                tasks = [get_lyrics(session, song["url"]) for song in page_songs]
                lyrics_list = await asyncio.gather(*tasks)
                
                for song, lyrics in zip(page_songs, lyrics_list):
                    songs.append({
                        "title": song["title"],
                        "url": song["url"],
                        "paroles": lyrics
                    })
                    print(f"Page {page}. Titre de la chanson : {song['title']}")
                
                print(f"Page {page} terminée - {len(page_songs)} chansons traitées")
                
    except Exception as e:
        print(f"Une erreur générale est survenue: {e}")
        
    finally:
        if songs:  # Sauvegarder uniquement si nous avons des données
            songs_df = pd.DataFrame(songs)
            file_name = f"{artist.strip().replace(' ', '_')}.csv"
            songs_df.to_csv(file_name, index=False, encoding="utf-8")
            print(f"Données sauvegardées - Total de {len(songs)} chansons")
        
        if driver:
            driver.quit()

if __name__ == "__main__":
    asyncio.run(main())