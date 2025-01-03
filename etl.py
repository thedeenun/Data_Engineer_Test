import requests
import re
import boto3
import os
import json
from dotenv import load_dotenv

load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
AWS_ACCESS_KEY=os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY=os.getenv("AWS_SECRET_KEY")

source_url = 'https://sasom-data-lake-bucket.s3.ap-southeast-1.amazonaws.com/test-data/samba.json'

def extract_data(url) -> dict: 
    req = requests.get(url=url)
    data = req.json()
    return data[0]

def transform_data(data) -> dict:
    transformed_data = dict()
    # Extract Product Data 
    product_data = dict()
    product_data['id'] = data.get('id')
    product_data['brand'] = data.get('brand')
    product_data['model'] = data.get('model')
    product_data['title'] = data.get('title')
    product_data['type'] = data.get('contentGroup')
    product_data['description'] = data.get('description')
    product_data['gender'] = data.get('gender')
    product_data['style'] = data.get('styleId')
    product_data['colorway'] = data.get('traits')[1].get('value')
    product_data['retail price'] = "$"+str(data.get('traits')[2].get('value'))
    product_data['release date'] = data.get('traits')[3].get('value')
    product_data['imageUrl'] = data.get('media').get('imageUrl')

    # Extract size and price
    size_and_price_data = []
    for sizes, price in zip(data['variants'], data['pricing']['variants']):
        record_temp = dict()
        if sizes['id'] == price['id']:
            record_temp['id'] = sizes['id']
            record_temp['sizes'] = []
            for s in sizes['sizeChart']['displayOptions']:
                temp_dict = {}
                size_type = re.findall('US M|US W|EU|KR|CM|UK', s.get('size'))[0]
                temp_dict[size_type] = " ".join(re.findall('[^US M|US W|EU|KR|CM|UK]+', s.get('size')))
                record_temp['sizes'].append(temp_dict)
            
            record_temp['price'] = price['market']['salesInformation']['lastSale']
            try:
                record_temp['lowerAsk'] = price['market']['state']['lowestAsk']['amount']
            except Exception:
                record_temp['lowerAsk'] = None
            try:
                record_temp['highestBid'] = price['market']['state']['highestBid']['amount']
            except Exception:
                record_temp['highestBid'] = None
        size_and_price_data.append(record_temp)
        
    
    transformed_data['product'] = product_data
    transformed_data['size by price'] = size_and_price_data
    
    return transformed_data

def load_to_s3(transformed_data):
    s3 = boto3.resource('s3',
                        endpoint_url='https://s3.ap-southeast-1.amazonaws.com',
                        aws_access_key_id=AWS_ACCESS_KEY,
                        aws_secret_access_key=AWS_SECRET_KEY)

    if s3.Bucket(BUCKET_NAME) not in s3.buckets.all():
        s3.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': 'ap-southeast-1'})

    json_data = json.dumps(transformed_data)

    object_key = 'sasom-etl-test.json'
    try:
        s3.meta.client.put_object(Bucket=BUCKET_NAME, Key=object_key, Body=json_data, ACL='public-read', ContentType='application/json')
        print(f"Data successfully uploaded to s3://{BUCKET_NAME}/{object_key}")
    except Exception as error:
        print(f"Error uploading data to S3: {error}")

if __name__ == "__main__":
    data = extract_data(url=source_url)
    transformed_data = transform_data(data)
    load_to_s3(transformed_data)