import argparse
import requests
import pickle
from constants import LOCAL_DIR




def get_response(endpoint_url):
    response = requests.get(endpoint_url, 'html')
    filename = endpoint_url.split('/')[-1]


def format_url(filename):
    return 


def save_response_to_disk(response):
    with open(LOCAL_DIR+filename, 'wb') as f:
        pickle.dump(response, f)
        

def main():
    parser = argparse.ArgumentParser('Retry endpoint urls')
    parser.add_argument('--ifile', metavar='i')
    parser.add_argument('--odir', metavar='o')
    args = parser.parse_args()

