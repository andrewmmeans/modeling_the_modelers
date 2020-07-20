from bs4 import BeautifulSoup
import requests
import argparse
import logging
import re


BASE_URL = 'https://www.cgtrader.com/3d-models/'
#CAT_TXT = '../data/categories.txt'


class CgtraderScraper():
    
    def __init__(self):
        self.categories = self._fetch_categories(BASE_URL)


    def _fetch_categories(self, url):
        """
        Fetches current categories on cgtrader's 3d-models page

        parameters:
        -----------
        url: str
            Top level url of page to grab categories from
        
        returns:
        --------
        url_model_categories: list(str)
            A list of category urls on cgtrader
        """
        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Use of set prevents duplicates
        url_model_categories = set()
        cpattern = re.compile(f"^{BASE_URL}")
        for link in soup.findAll('a', attrs={'href': cpattern}):
            url_model_categories.add(link.get('href'))

        return list(url_model_categories)    


    def _fetch_url(self, url):
        response = requests.get(url)
        return response    


    def _get_soup(self, response):
        soup = BeautifulSoup(response.content, 'html')
        return soup


    def _make_soup(self, url):
        response = self._fetch_url(url)
        soup = self._get_soup(response)
        return soup


    def _scrape_categories(self):
        soup = self._make_soup(BASE_URL)
        url_model_categories = set()
        for link in soup.findAll('a', attrs={'href': re.compile(f"^{BASE_URL}")}):
            url_model_categories.add(link.get('href'))
        return url_model_categories

    
def main():
    cgscraper = CgtraderScraper()
    print(cgscraper.categories)


if __name__ == '__main__':
    main()