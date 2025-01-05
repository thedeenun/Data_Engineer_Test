import os
import httpx
import asyncio
import json
from nested_lookup import nested_lookup
from parsel import Selector
from fake_useragent import UserAgent
ua = UserAgent()


client = httpx.AsyncClient(
    http2=True,
    follow_redirects=True,
    headers={
        # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "User-Agent": f"{ua.random}"
    },
)

async def fetch_url(url):
    response = await client.get(url)
    if response.status_code == 200:
        print(f"Fetch {url} succeeded")
        with open("sources/stockx_nike_dunk.html", "w") as file:
            file.write(response.text)
    else:
        print(f"Fetch {url} unsucceeded: Status code {response.status_code}")

if __name__ == '__main__':
    url = 'https://stockx.com/nike-dunk-low-retro-white-black-2021'
    asyncio.run(fetch_url(url))

    if os.path.exists("sources/stockx_nike_dunk.html"):    
        file = open("sources/stockx_nike_dunk.html", "r")
        selector = Selector(file.read())

    data_json = json.loads(selector.xpath('//*/script[@id="__NEXT_DATA__"]//text()').get())
    products_json = nested_lookup("product", data_json)[0]

    product_data = dict()
    
    product = dict()
    product['id'] = products_json.get('id')
    product['brand'] = products_json.get('brand')
    product['model'] = products_json.get('model')
    product['title'] = products_json.get('title')
    product['type'] = products_json.get('contentGroup')
    product['description'] = products_json.get('description')
    product['gender'] = products_json.get('gender')
    product['style'] = products_json.get('styleId')
    product['colorway'] = products_json.get('traits')[1].get('value')
    product['retail price'] = "$"+str(products_json.get('traits')[2].get('value'))
    product['release date'] = products_json.get('traits')[3].get('value')
    product['imageUrl'] = products_json.get('media').get('imageUrl')

    size_by_price = products_json['variants']
    product_data['product'] = product
    product_data['size_by_price'] = size_by_price
    
    with open("data/stockx_nike_dunk.json", "w") as file:
        file.write(json.dumps(product_data, indent=4))


