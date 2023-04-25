import trafilatura

from helpers import getLogger
from scraping.helpers import *
from scraping.database import Database

logger = getLogger(__name__)
db = Database(database_name='',
              endpoint='',
              username='',
              password='',
              port='',
              type='postgres')

class ShopifyJsonScraper:

    def __init__(self,
                 url,
                 website_name):
        self.url = url
        self.website_name = website_name
        self.text_per_product_dict = {}

    def scrapeJson(self):
        response = requests.get('http://thegoodgood.co/products.json')
        json_data = response.json()['products']

        # Initialize lists to store data for each table
        products_data = []
        tags_data = []
        variants_data = []
        product_options_data = []
        product_tags_data = []

        tag_id_map = {}

        for item in json_data:
            # Extract product data
            product = {
                "id": item["id"],
                "title": item["title"],
                "handle": item["handle"],
                "description": trafilatura.extract(item["body_html"]),
                "published_at": item["published_at"],
                "created_at": item["created_at"],
                "updated_at": item["updated_at"],
                "vendor": item["vendor"],
                "product_type": item["product_type"],
            }
            products_data.append(product)

            # Extract tags data
            for tag in item["tags"]:
                if tag not in tag_id_map:
                    tag_id_map[tag] = len(tag_id_map) + 1
                    tags_data.append({"id": tag_id_map[tag], "name": tag})

                # Extract product_tags data
                product_tags_data.append({"product_id": item["id"], "tag_id": tag_id_map[tag]})

            # Extract variants data
            for variant in item["variants"]:
                variant["product_id"] = item["id"]
                variants_data.append(variant)

            # Extract product options data
            for option in item["options"]:
                product_option = {
                    "product_id": item["id"],
                    "name": option["name"],
                    "position": option["position"],
                }
                product_options_data.append(product_option)

        self.products_df = pd.DataFrame(products_data)
        self.tags_df = pd.DataFrame(tags_data)
        self.variants_df = pd.DataFrame(variants_data)
        self.product_options_df = pd.DataFrame(product_options_data)
        self.product_tags_df = pd.DataFrame(product_tags_data)

    def formatJsonText(self):
        return False

    def getDocsList(self):
        self.page_docs_list = []
        for product_dict in self.products_df.to_dict('records'):
            string_to_add = f"""This is the description for product {product_dict['title']}: \n
            {product_dict['description']}"""
            self.page_docs_list.append(string_to_add)

    def push(self):

        db.upsert(df=self.products_df, table_name='products', primary_key=['id'])
        db.upsert(df=self.tags_df, table_name='tags', primary_key=['id'])
        db.upsert(df=self.product_options_df, table_name='product_options', primary_key=['product_id', 'name'])
        db.upsert(df=self.variants_df, table_name='variants', primary_key=['id'])
        db.upsert(df=self.product_tags_df, table_name='product_tags', primary_key=['product_id', 'tag_id'])
        logger.info("Upserted store data to database")
    def run(self):
        self.scrapeJson()
        self.getDocsList()
        self.push()
