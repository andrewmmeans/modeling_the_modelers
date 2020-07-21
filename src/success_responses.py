import requests
import pickle
from constants import DATA_DIR
import os
from multiprocessing import Pool



def is_success(response):
    return response.status_code == 200


def save_to_file(name, response, odir):
    with open(odir+name, 'wb') as f:
        pickle.dump(response, f)


def process_response(filename):
    with open(DATA_DIR+'cgtrader/'+filename, 'rb') as f:
        response = pickle.load(f)
        if is_success(response):
            save_to_file(filename, response, DATA_DIR+'success/')


if __name__ == '__main__':
    response_files = os.listdir(DATA_DIR + 'cgtrader/')
    with Pool(8) as p:
        p.map(process_response, response_files)
        