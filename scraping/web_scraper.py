import time

import trafilatura
from trafilatura.sitemaps import sitemap_search

from helpers import getLogger

logger = getLogger(__name__)


def extract_text_from_page(url):
    while True:
        try:
            fetched_page = trafilatura.fetch_url(url)
            text = trafilatura.extract(fetched_page, include_comments=False)
            return text
        except Exception as e:
            if "430 Client Error" in str(e):
                print(f"Too many requests. Waiting 5 seconds before trying again.")
                time.sleep(60)
            else:
                raise e


class ShopifyWebScraper:

    def __init__(self,
                 url,
                 website_name):
        self.url = url
        self.website_name = website_name
        self.fetched_texts_dict = {}
        self.formatted_texts_dict = {}

    def scrapeWeb(self):
        logger.info(f"Scraping {self.website_name} website: {self.url}.")
        self.sitemap_urls = sitemap_search(self.url)
        self.sitemap_urls = [url for url in self.sitemap_urls if 'https://www.thegoodgood.co/products' not in url]

        for url in self.sitemap_urls:
            extracted_text = extract_text_from_page(url)
            self.fetched_texts_dict[url] = extracted_text
            logger.info(f"Extracted {len(self.fetched_texts_dict.keys())}/{len(self.sitemap_urls)} texts.")
            time.sleep(1)

    def formatWebText(self):
        logger.info(f"Formatting {self.website_name} website texts.")
        for url, text in self.fetched_texts_dict.items():
            extracted_text = extract_text_from_page(url)
            text_to_input = f"""
            This text is extracted from {url} on the {self.website_name} E-commerce store:
            {extracted_text}
            """
            self.formatted_texts_dict[url] = text_to_input

    def processDocList(self):
        return False

    def getDocsList(self):
        logger.info(f"Getting {self.website_name} website vector store.")
        self.page_docs_list = list(self.formatted_texts_dict.values())

        self.processDocList()

    def run(self):
        self.scrapeWeb()
        self.formatWebText()
        self.getDocsList()
