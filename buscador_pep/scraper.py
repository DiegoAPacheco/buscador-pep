import time
from enum import Enum  # Se importa Enum

from bs4 import BeautifulSoup
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from buscador_pep.config import UserProfile

class WebDriverState(Enum):
    UNOPERATIVE = "Unoperative"
    READY = "Ready"
    RUNNING = "Running"
    STOPPED = "Stopped"

class Scraper:
    def __init__(self, url: str, user_profile: UserProfile, driver: WebDriver):
        self.url = url
        self.user_profile = user_profile
        self.driver = driver
        self.state = WebDriverState.UNOPERATIVE

    def start(self) -> None:
        if self.state == WebDriverState.UNOPERATIVE:
            self.driver.get(self.url)
        else:
            raise ValueError("El scraper ya está en funcionamiento")
        
        invalid_user_filters = self._get_invalid_user_filters()
        if len(invalid_user_filters) == 0: 
            self.state = WebDriverState.READY
        else:
            self.state = WebDriverState.STOPPED
            raise ValueError(f"Los filtros de usuario son inválidos: {invalid_user_filters}")
        
    def _read_filter(self, filter_id: str) -> list[str]:
        options = []
        # Caso especial para comboAreas (select)
        if "comboAreas" in filter_id:
            try:
                select_element = self.driver.find_element(
                    By.XPATH, "//select[contains(concat(' ', normalize-space(@class), ' '), ' comboAreas ')]"
                )
                # Extraer opciones del select (omitir la opción predeterminada si se requiere)
                for option in select_element.find_elements(By.TAG_NAME, "option"):
                    text = option.text.strip()
                    if text:
                        options.append(text)
            except Exception:
                return []
            return options
        # Para dropdowns: construir XPATH para <div> con todas las clases y buscar el <ul> hijo con clase "dropdown-menu"
        classes = filter_id.split()
        conditions = " and ".join(
            f"contains(concat(' ', normalize-space(@class), ' '), ' {cls} ')" for cls in classes
        )
        xpath_ul = f"//div[{conditions}]/ul[contains(concat(' ', normalize-space(@class), ' '), ' dropdown-menu ')]"
        try:
            ul = self.driver.find_element(By.XPATH, xpath_ul)
        except Exception:
            return []
        li_elements = ul.find_elements(By.XPATH, "./li")
        for li in li_elements:
            try:
                a = li.find_element(By.XPATH, ".//a[@role='menuitem']")
                text = a.text.strip()
                if text:
                    options.append(text)
            except Exception:
                continue
        return options

    def _get_filters(self) -> dict[str, list[str]]:
        return {
            "location": self._read_filter("dropdown regiones"),
            "industry": self._read_filter("comboAreas"), # Este caso requiere una excepción
            "job_opening_status": self._read_filter("dropdown dropdown-estados"),
            "job_category": self._read_filter("dropdown dropdown-cargo"),
            "pay_range": self._read_filter("dropdown rentas"),
            "legal_status": self._read_filter("dropdown calidades"),
        }
    
    def _get_invalid_user_filters(self) -> list[str]:
        invalid_filters = []
        filters = self._get_filters()
        for filter_name, filter_values in filters.items():
            if getattr(self.user_profile.filters, filter_name) not in filter_values:
                invalid_filters.append(filter_name)
        return invalid_filters

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
