import os
from dotenv import load_dotenv

load_dotenv('config.env')
API_KEY = os.getenv('API_KEY')
ORGANIZATION_ID = os.getenv('ORGANIZATION_ID')
MAX_SEQUENCE_NUMBER = os.getenv('MAX_SEQUENCE_NUMBER')