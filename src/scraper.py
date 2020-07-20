import requests
import re
from bs4 import BeautifulSoup


class Scraper():

    def __init__(self):
        pass

    def _fetch_url(self, url):
        response = requests.get(url)
        return response    


    def _get_soup(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup


    def fetch_url(self, url):
        return self._fetch_url(url)


    def make_soup(self, url):
        response = self._fetch_url(url)
        soup = self._get_soup(response)
        return soup