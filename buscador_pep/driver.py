from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

def get_driver():
    options = Options()
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    return driver