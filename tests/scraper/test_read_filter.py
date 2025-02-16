import pytest
from unittest.mock import MagicMock
from selenium.webdriver.common.by import By

# Asumir que Scraper se importa de la siguiente forma:
from buscador_pep.scraper import Scraper

class DummyUserProfile:
    filters = type("obj", (), {"location": "Todas las regiones", "industry": "", "job_opening_status": "",
                                "job_category": "", "pay_range": "", "legal_status": ""})

# Helper para crear una instancia de Scraper con driver simulado.
@pytest.fixture
def scraper():
    dummy_driver = MagicMock()
    return Scraper(url="http://dummy", user_profile=DummyUserProfile(), driver=dummy_driver)

def test_read_filter_comboAreas(scraper):
    # Simular el comportamiento para un <select> de comboAreas.
    # Se simula una lista de opciones con textos.
    fake_option1 = MagicMock()
    fake_option1.text = "Área 1"
    fake_option2 = MagicMock()
    fake_option2.text = "Área 2"
    fake_select = MagicMock()
    fake_select.find_elements.return_value = [fake_option1, fake_option2]

    # Configurar el método find_element para comboAreas
    scraper.driver.find_element.return_value = fake_select

    result = scraper._read_filter("comboAreas")
    assert result == ["Área 1", "Área 2"]
    # Verificar que se llamó con el XPATH correcto
    scraper.driver.find_element.assert_called_with(By.XPATH, 
        "//select[contains(concat(' ', normalize-space(@class), ' '), ' comboAreas ')]")

def test_read_filter_dropdown(scraper):
    # Simular el comportamiento para un dropdown normal, ej. "dropdown regiones".
    # Se crea un fake ul que devuelve varios li con elementos <a role="menuitem">
    fake_a1 = MagicMock()
    fake_a1.text = "Todas las regiones"
    fake_a2 = MagicMock()
    fake_a2.text = "Arica y Parinacota"
    
    fake_li1 = MagicMock()
    fake_li1.find_element.return_value = fake_a1
    fake_li2 = MagicMock()
    fake_li2.find_element.return_value = fake_a2

    fake_ul = MagicMock()
    fake_ul.find_elements.return_value = [fake_li1, fake_li2]

    # Configurar: al buscar el ul vía XPATH se devuelve fake_ul.
    scraper.driver.find_element.return_value = fake_ul

    result = scraper._read_filter("dropdown regiones")
    assert result == ["Todas las regiones", "Arica y Parinacota"]

def test_read_filter_exception(scraper):
    # Simular que driver.find_element lanza una excepción al buscar el <ul>
    scraper.driver.find_element.side_effect = Exception("Elemento no encontrado")
    result = scraper._read_filter("dropdown regiones")
    assert result == []
