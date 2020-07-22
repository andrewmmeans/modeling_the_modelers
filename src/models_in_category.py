import requests




def parse_category_page(category_page):
    response = requests.get(category_page)
    model_urls_and_titles = re.findall('(?i)<a href=\"(https:\/\/www.cgtrader.com\/3d-models\/[a-z]+\/[^>]+)" title="([^"]+)', str(response.content))
    return model_urls_and_titles