import json
import requests
import os
import boto3
from dotenv import load_dotenv
from datetime import datetime
from botocore.exceptions import NoCredentialsError, ClientError

class RainforestAPI:
    def __init__(self, api_key=None):
        # Load environment variables
        load_dotenv()

        # Use provided API Key or get it from environment variables
        self.api_key = api_key or os.getenv('RAINFOREST_API_KEY')
        self.base_url = 'https://api.rainforestapi.com/request'

    def get_search_results(self, keyword):
# Need to handle if keyword has special characters

        params = {
            'api_key': self.api_key,
            'type': 'search',
            'amazon_domain': 'amazon.com',
            'search_term': keyword
        }

        try:
            api_result = requests.get(self.base_url, params)
            api_result.raise_for_status() # Check for HTTP errors
            return api_result.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

class JSONStorageS3:
    def __init__(self, bucket_name='rf-search-results'):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def store(self, data, keyword):
        current_timestamp = datetime.now()
        date_string = current_timestamp.strftime("%Y-%m-%d")
        
        no_space_kw = keyword.replace(' ', '_')

        folder_name = f'{no_space_kw}'
        file_name = f'search_results_{no_space_kw}_{date_string}.json'
        s3_key = f'{folder_name}/{file_name}'

        json_data = json.dumps(data, indent=4)

        try:
            self.s3.put_object(Bucket=self.bucket_name, Key=s3_key, Body=json_data)
            print(f'Data has been uploaded to s3 at {s3_key}')
        except NoCredentialsError:
            print("Credentials not available.")
        except ClientError as e:
            print(f'An error occurred: {e}')

if __name__ == '__main__':
    api = RainforestAPI()
    storage = JSONStorageS3()

    keyword = 'grass seed'
    
    print(f'Retrieving results for {keyword}')

    results = api.get_search_results(keyword)

    if results:
        print(f'Successfully retrieved results for {keyword}')
        storage.store(results, keyword)
    else:
        print('No results were retrieved')


# def lambda_handler(event, context):
#     # Example keyword from the event data
#     keyword = event.get('keyword', 'default')

#     # Create instances of your classes
#     api = RainforestAPI()
#     storage = JSONStorageS3()

#     # Get search results
#     results = api.get_search_results(keyword)

#     # If results are retrieved successfully, store them
#     if results:
#         storage.store(results, keyword)
#     else:
#         print("No results were retrieved.")

#     return {
#         'statusCode': 200,
#         'body': json.dumps('Process completed')
#     }
