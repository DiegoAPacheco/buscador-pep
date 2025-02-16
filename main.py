from pathlib import Path

from buscador_pep.scraper import Scraper
from buscador_pep.driver import get_driver
from buscador_pep.llm_filter import filter_offers
from buscador_pep.config import read_configuration



def main():
    config = read_configuration(Path("config.toml"))
    
    scraper = Scraper(config.portal_url, config.user_profile, get_driver())

    scraper.start()
    
    offers = scraper.get_offers()
    
    filtered_offers = filter_offers(offers, config.user_profile)
    
    for offer in filtered_offers:
        print(offer)

if __name__ == "__main__":
    main()
