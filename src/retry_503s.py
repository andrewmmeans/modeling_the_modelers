from multiprocessing import Pool
import argparse
import requests
import pickle
import os


folder = '/home/void/github/gal/capstones/modeling_the_modelers/data/'
outdir = '/home/void/data/success/'

files = os.listdir(folder)
success_files = os.listdir(outdir)

urls_to_fetch_again = []


def is_duplicate(url):
    return url.split('/')[-1] in success_files


def process_files(files):
    for i, file in enumerate(files):
        if file.endswith('model_urls'):
            with open(folder+file, 'rb') as f:
                urls = pickle.load(f)
            for url in urls:
                if not is_duplicate(url):
                    try:
                        response = requests.get(url)
                        if response.status_code == 200:
                            with open(outdir + url.split('/')[-1], 'wb') as f:
                                pickle.dump(response, f)
                        else:
                            urls_to_fetch_again.append(response.url)
                    except Exception as e:
                        print(f'Exception {e}')

                else:
                    print(f'Already retrieved {url}')
    # with open(f'/home/void/data/','wb') as f:
    #     pickle.dump(urls_to_fetch_again, f)



def main(folder):
    process_files(files)

    


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Retry 503 requests')
    #parser.add_argument('ind', metavar='in', type=str)
    #parser.add_argument('outd', metavar='out', type=str)
    #parser.add_argument('replace', metavar='r', type=str)
    #args = parser.parse_args()
    main(folder)

