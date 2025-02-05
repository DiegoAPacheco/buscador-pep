from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

def get_driver() -> WebDriver:
    options = Options()
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    return driver