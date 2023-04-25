import os
import requests
from logging import getLogger

from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import Chroma

from scraping.json_scraper import ShopifyJsonScraper
from scraping.web_scraper import ShopifyWebScraper

logger = getLogger(__name__)
embeddings = OpenAIEmbeddings()


def joinPaths(paths: list):
    # Remove '/' at the beginning of all paths
    paths = [path[1:] if path.startswith('/') and i != 0 else path for i, path in enumerate(paths)]
    return os.path.join(*paths)


class StoreScraper:

    def __init__(self,
                 url,
                 vector_store_dir_path
                 ):
        self.url = url
        self.website_name = requests.get("https://bajauswim.com/meta.json").json()['name']
        self.text_per_product_dict = {}
        vector_store_dir_path = vector_store_dir_path
        vector_store_file_name = f"{self.website_name.replace(' ', '')}_vector_store"
        self.vector_store_file_path = joinPaths([vector_store_dir_path, vector_store_file_name])
        self.doc_string_list = []

    def scrape(self,
               web=True,
               json=True):
        if json is True:
            self.json_scraper = ShopifyJsonScraper(self.url, self.website_name)
            self.json_scraper.run()
            self.doc_string_list += self.json_scraper.page_docs_list

        if web is True:
            self.webscraper = ShopifyWebScraper(self.url, self.website_name)
            self.webscraper.run()
            self.doc_string_list += self.webscraper.page_docs_list

    def uploadVectoreStore(self):
        # Save and persis data
        self.doc_string_list = [Document(page_content=text) for text in self.doc_string_list]
        vectordb = Chroma.from_documents(documents=self.doc_string_list, embedding=embeddings,
                                         persist_directory=self.vector_store_file_path)
        vectordb.persist()
        logger.info(f"Saving {self.website_name} JSON data vectore store")

    def run(self,
            web=True,
            json=True
            ):
        self.scrape(web,
                    json)
        self.uploadVectoreStore()
