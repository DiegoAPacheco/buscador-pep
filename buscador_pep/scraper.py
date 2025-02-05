import time

from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver

class Scraper:
    def __init__(self, url: str, driver: WebDriver):  # se agrega driver como parámetro
        self.url = url
        self.driver = driver

    def get_offers(self) -> list[str]:
        # Usar Selenium para cargar contenido dinámico con el driver proporcionado
        self.driver.get(self.url)
        time.sleep(5)  # Espera a que la página cargue completamente el contenido dinámico
        page_source = self.driver.page_source
        # No se cierra el driver aquí, se gestiona externamente
        # Parsear el contenido HTML obtenido
        soup = BeautifulSoup(page_source, "html.parser")
        offers = []
        # ... código de parseo de las ofertas ...
        # Ejemplo abstracto: suponer que cada oferta es un div con clase 'job-offer'
        for div in soup.find_all("div", class_="job-offer"):
            title = div.find("h2").get_text(strip=True) if div.find("h2") else "Sin título"
            offers.append({
                "title": title,
                # ...otros campos relevantes...
            })
        return offers
