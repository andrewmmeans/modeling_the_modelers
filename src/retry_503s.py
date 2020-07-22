import argparse
import pickle



folder = '~/data/cgtrader'

files = os.listdir(folder)

urls_to_fetch_again = []

def main(folder):
    for i, file in enumerate(files):
        with open('/home/void/data/cgtrader/'+file, 'rb') as f:
            response = pickle.load(f)
            if response.status_code != 200:
                urls_to_fetch_again.append(response.url)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retry 503 requests')
    parser.add_argument('ind', metavar='in', type=str)
    parser.add_argument('outd', metavar='out', type=str)
    parser.add_argument('replace', metavar='r', type=str)
    args = parser.parse_args()

