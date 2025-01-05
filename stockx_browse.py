import re
import os
import pandas as pd
import httpx
import asyncio
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

def get_product_browse(response):
    selector = Selector(response)
    name_list = [" ".join(re.findall('\w+',name)) for name in selector.xpath('//*/div[@id="product-results"]/div[@data-component="brand-tile"]//div[@data-testid="product-details"]/div[1]/p/text()').getall()]
    link_list = ["https://stockx.com"+link for link in selector.xpath('//*/div[@id="product-results"]/div[@data-component="brand-tile"]//a/@href').getall()]

    return name_list, link_list

async def fetch_url(url):
    try:
        response = await client.get(url)
        if response.status_code == 200:
            print(f"Fetch {url} succeeded")
            return response.text, response.status_code
        else:
            print(f"Skipping URL {url}: Status code {response.status_code}")
            return None, response.status_code
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {url}: {e}")

async def main():
    product_list = []
    start_page = 1
    end_page = 25
    for page in range(start_page, end_page+1):
        url = f"https://stockx.com/category/sneakers?page={page}"
        response_text, status_code = await fetch_url(url)
        if status_code != 200:
            continue
        name_list, link_list = get_product_browse(response_text)
        
        for nl, ll in zip(name_list, link_list):
            product_list.append((nl, ll))  

    product_browse_df = pd.DataFrame(product_list, columns=["product_name", "product_link"])
    if os.path.exists('data/stockx_browse.csv'):
        product_browse_df_read = pd.read_csv('data/stockx_browse.csv')
        product_browse_df_merge = pd.concat([product_browse_df_read, product_browse_df])
        product_browse_df_merge.drop_duplicates(inplace=True)
        product_browse_df_merge.to_csv('data/stockx_browse.csv', index=False)
    else:
        product_browse_df.to_csv('data/stockx_browse.csv', index=False)

if __name__ == '__main__':
    asyncio.run(main())
