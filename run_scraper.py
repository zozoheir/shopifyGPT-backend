from scraping.store_scraper import StoreScraper

URL = "https://bajauswim.com/"
VECTOR_STORE_DIR_PATH = "/Users/othmanezoheir/tmp/shopify/vector_stores/"

store_scraper = StoreScraper(
    url=URL,
    vector_store_dir_path=VECTOR_STORE_DIR_PATH
)

store_scraper.run(web=True,
                  json=True
                  )
