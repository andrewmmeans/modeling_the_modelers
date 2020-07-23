from bs4 import BeautifulSoup
import requests
from constants import DATA_DIR
from multiprocessing import Pool
import pandas as pd
import pickle
import json
import re
import os

from datetime import datetime


def is_svg_checked(tag):
    return 'is-green' in str(tag)


def get_tags(soup):
    tags = list(map(lambda x: x.text, soup.select('li.label')))
    return tags


def get_views(soup):
    views_str = soup.select('.stats-info__views-button')[0].attrs.get('content').split(' ')[0]
    views = convert_str_num_to_int(views_str, 'shorthand')
    return views


def get_likes(soup):
    like_count = 0
    try:
        like_count = int(soup.select('.stats-info__like-button > div:nth-child(1)')[0].attrs.get('content').split(' ')[0])
    except:
        print(soup.select('.stats-info__like-button > div:nth-child(1)'))
    return like_count


def get_price(soup):
    return soup.select('.product-pricing__price > span:nth-child(1) > span:nth-child(1)')[0].text


def get_pic_count(soup):
    pic_count = 0
    try:
        pic_count = int(soup.select('.footerCount')[0].text.split('/')[1].strip())
    except IndexError as e:
        print(soup.select('.footerCount'))
    return pic_count



def get_comments(soup):
    comments = soup.select('.comments-list')[0]
    comment_authors = list(map(lambda x: x.text, comments.select('.author-link')))
    comment_texts = list(map(lambda x: x.text[:-5], comments.select('.card')))
    comment_datetimes = list(map(lambda x: datetime.strptime(x.text, '%Y-%m-%d %H:%M'), comments.select('.project-comment__date')))
    comments_dict = {
        'authors': comment_authors, 
        'texts': comment_texts, 
        'datetimes': comment_datetimes
    }
    return comments_dict


def get_model_review_count(soup):
    review_count = 0
    try:
        review_count = int(soup.select('.js-reviews-section')[0].text.split(' ')[1][1:-1])
    except Exception as e:
        print(f"Failure in get_model_review_count: {e}")
    return review_count


def get_modeler(soup):
    return soup.select('.username')[0].text


def get_modeler_ratings(soup):
    ratings = {
        'avg_rating': json.loads(soup.select('div.author-rating > div:nth-child(1)')[0].attrs.get('data-react-props')).get('rating'),
        'num_rating': int(soup.select('.link--primary')[0].text[1:-1].split(' ')[0])
    }
    return ratings


def get_modeler_response(soup):
    response_arr = soup.select('.author-response > span:nth-child(2)')[0].text.split(' ')
    percent = 0
    time = 0
    try:
        percent = int(response_arr[0][:-1])
        time = response_arr[2]
    except:
        pass
    response = {
        'percent': percent,
        'time': time
    }
    return response


def get_model_description(soup):
    description = soup.select('.product-description')[0].text.replace('\n', ' ')
    return description
    

def get_model_formats(soup):
    format_body = soup.select('ul.info-list')[0]
    formats = [x.text for x in format_body.select('.js-format-link')]
    sizes = [x.text for x in format_body.select('.right-column')]
    format_dict = {
        'formats': formats,
        'sizes': sizes
    }
    return format_dict


def convert_str_num_to_int(string, str_type='comma'):
    num = 0
    if str_type == 'comma':
        try:
            num = int(''.join(string.split(',')))
        except:
            pass
        return num
    elif str_type == 'shorthand':
        if string[-1] == 'k':
            num = int(float(string[:-1]) * 1000)
        else:
            num = int(string)
    return num


def get_model_details(soup):
    info_list = soup.select('ul.info-list')
    model_detail_section = info_list[-1]
    publish_date = datetime.strptime(model_detail_section.select('.right-column')[0].text, '%Y-%m-%d')
    model_id = model_detail_section.select('.right-column')[1].text.split('#')[1]
    bool_cols = ['animated', 'rigged', 'vr/ar/low-poly', 'pbr', 'textures', 'materials', 'uv_mapping', 'plugins_used']
    bool_vals = list(map(lambda x: 'is-green' in str(x), model_detail_section.select('.fal')))
    bool_dict = {k: v for k, v in list(zip(bool_cols, bool_vals))}
    geometry = model_detail_section.select('.u-float-right')[4].text
    polygon_text = model_detail_section.select('.u-float-right')[5].text
    polygons = convert_str_num_to_int(polygon_text)
    vertice_text = model_detail_section.select('.u-float-right')[6].text
    vertices = convert_str_num_to_int(vertice_text)
    unwrapped_uvs = model_detail_section.select('.u-float-right')[10].text
    model_detail_dict = {
        'model_id':model_id,
        'geometry':geometry,
        'polygons':polygons,
        'vertices':vertices,
        'unwrapped_uvs':unwrapped_uvs
    }
    model_detail_dict.update(bool_dict)
    return model_detail_dict


def process_file(fname, subdir='success/'):
    model_dict = {}
    with open(DATA_DIR+subdir+fname, 'rb') as f:
        response = pickle.load(f)
        soup = BeautifulSoup(response.content, 'html.parser')
        model_dict = {
            'modeler':get_modeler(soup),
            'modeler_response':get_modeler_response(soup),
            'modeler_ratings':get_modeler_ratings(soup),
            'tags':get_tags(soup),
            'views':get_views(soup),
            'likes':get_likes(soup),
            'review_count': get_model_review_count(soup),
            'comments':get_comments(soup),
            'price':get_price(soup),
            'pic_count':get_pic_count(soup),
            'model_description': get_model_description(soup),
            'model_details':get_model_details(soup)        
        }
    return model_dict


def process_files(files, batch_num, odir='processed_files/', pool=True, nworkers=8):
    res = []
    if pool:
        with Pool(nworkers) as p:
            res.extend(p.map(process_file, files))
    else:
        for file in files:
            res.extend(process_file)
    df = pd.DataFrame(res)
    #df.to_csv(DATA_DIR + odir + f'model_pages_and_desc_{batch_num}.csv')
    df.to_pickle(DATA_DIR + odir + f'model_pages_and_desc_{batch_num}.pkl')


def main():
    success_files = os.listdir(DATA_DIR + 'success/')
    chunk_size = 1000
    chunks = (len(success_files) - 1) // chunk_size + 1
    batches = []
    for i in range(chunks):
        batch = success_files[i*chunk_size:(i+1)*chunk_size]
        batches.append(batch)
    for i, batch in enumerate(batches):
        if i > 48:
            try:
                process_files(batch, batch_num=i)
            except Exception as e:
                print(f'Batch {i} failed')
                print(e)

if __name__ == '__main__':
    main()
        