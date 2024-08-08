import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv('RAINFOREST_API_KEY')
another_variable = os.getenv('AWS_SECRET')

# Print the values to verify
print(f"RAINFOREST_API_KEY: {api_key}")
print(f"ANOTHER_VARIABLE: {another_variable}")

current_directory = os.getcwd()
print(f"Current working directory (workspace folder): {current_directory}")
