from pathlib import Path

from buscador_pep.scraper import Scraper
from buscador_pep.llm_filter import filter_offers
from buscador_pep.config import read_configuration
from buscador_pep.user_profile import read_user_profile



def main():
    config = read_configuration(Path("config.toml"))
    
    scraper = Scraper(config.portal_url)
    
    offers = scraper.get_offers()
    
    user_profile = read_user_profile(Path(config.user_profile_path))
    
    filtered_offers = filter_offers(offers, user_profile)
    
    for offer in filtered_offers:
        print(offer)

if __name__ == "__main__":
    main()
