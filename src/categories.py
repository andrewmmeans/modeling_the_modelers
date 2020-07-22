from cgtrader_scraper import CgtraderScraper
from scraper import Scraper
import requests
from multiprocessing import Pool
from constants import BASE_URL
import pickle
import re


class CategoryScraper(Scraper):

    def __init__(self, name):
        self.category_names_and_max_pages = {}
        self._load_categories_and_max_pages()
        self.name = name
        self.url = name.lower()
        self.pages_to_scrape = []
        self.model_urls = []


    def _load_categories_and_max_pages(self):
        with open('../data/cats_with_277_pages', 'rb') as f:
            categories_and_max_pages = pickle.load(f)
            self.category_urls_and_max_pages = {
                k: v for k, v in categories_and_max_pages
            }
            self.category_names_and_max_pages = {
                k.split('/')[-1]: [k, v] for k, v in categories_and_max_pages
            }


    def _validate_category(self):
        return self.name in list(self.category_names_and_max_pages.keys())


    def _format_url_pagination(self, url, page):
        return f"{url}?page={page}"


    def parse_category_page(self, category_page):
        response = requests.get(category_page)
        model_urls_and_titles = re.findall('(?i)<a href=\"(https:\/\/www.cgtrader.com\/3d-models\/[a-z]+\/[^>]+)" title="([^"]+)', response.text)
        return [x[0] for x in model_urls_and_titles]


    def build_pages_to_scrape(self):
        if self._validate_category():
            category, page = self.category_names_and_max_pages.get(self.name)
            for i in range(1, page):
                formatted_url = self._format_url_pagination(category, i)
                self.pages_to_scrape.append(formatted_url) 


    def parse_all_pages(self):
        with Pool(8) as p:
            res = p.map(self.parse_category_page, self.pages_to_scrape)
            self.model_urls.extend(res)


    def dedupe_models(self):
        model_urls = [y for x in self.model_urls for y in x]
        self.model_urls = list(set(model_urls))


    def save_model_urls(self):
        with open(f'../data/{self.name}_model_urls', 'wb') as f:
            pickle.dump(self.model_urls, f)


def main(category):
    cs = CategoryScraper(category)
    cs.build_pages_to_scrape()
    cs.parse_all_pages()
    cs.dedupe_models()
    cs.save_model_urls()


if __name__ == '__main__':
    with open('../data/cats_with_277_pages', 'rb') as f:
        categories_and_max_pages = pickle.load(f)
        category_names_and_max_pages = {
            k.split('/')[-1]: [k, v] for k, v in categories_and_max_pages
        }

    for category in list(category_names_and_max_pages.keys())[0:2]:
        main(category)
        # cs = CategoryScraper(category)
        # cs.build_pages_to_scrape()
        # t.extend(cs.parse_category_page(cs.pages_to_scrape[0]))
        # break
    #cs.parse_all_pages()

    



    

    
