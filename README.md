# Sasom_Data_Engineer
This test project is including in technical interview By Sasom in Data Engineer Role, the project consists of 2 section, including Scraping project and ETL project

## Scraping Projcet
Scrape these 3 websites StockX, Poizon, and SNKR DUNK

**StockX**
- 1st target_url: https://stockx.com/category/sneakers for browse all product_link in many pages
- 2nd target_url: https://stockx.com/nike-dunk-low-retro-white-black-2021 for spacific product page
- using httpx and asyncio to request javascript render
    - python script:
        - stockx_browse.py
        - stockx_scraping.py
    - scraped_data:
        - data/stockx_browse.csv
        - data/stockx_nike_dunk.json (this scraped_data not complete!, I cannot fetch pricing data from XHR)

**Poizon**
- target_url: https://www.poizon.com/product/nike-dunk-low-panda-black-white-52581981
- using Selenium to request url to handle with invisable and clicking
    - python script: poizon_scraping.py
    - scraped_data: data/poizon_size-guide.csv

**SNKR DUNK**
- target_url: https://snkrdunk.com/en/sneakers/DD1391-100
- using Selenium to request url to handle with invisable and clicking
    - python script: snkr_dunk_scraping.py
    - scraped_data: 
        - data/snkr_dunk_men-size.csv
        - data/snkr_dunk_women-size.csv
        - data/snkr_dunk_price-by-size.csv

## ETL Project
- read data from: https://sasom-data-lake-bucket.s3.ap-southeast-1.amazonaws.com/test-data/samba.json
- transformed all basic product detail into product data, for example product_id, title, description, style, colorway and etc.
- transformed size by price by matching variants_id for size and variants_id for price of the product and collect to list of dictionary
- load transformed data to my s3: https://adeenun-data.s3.ap-southeast-1.amazonaws.com/sasom-etl-test.json