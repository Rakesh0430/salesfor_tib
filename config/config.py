# config/config.py

import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.client_id = os.getenv("SALESFORCE_CLIENT_ID")
        self.client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")
        self.username = os.getenv("SALESFORCE_USERNAME")
        self.password = os.getenv("SALESFORCE_PASSWORD")
        self.token_url = os.getenv("SALESFORCE_TOKEN_URL", "https://login.salesforce.com/services/oauth2/token")
        self.api_version = os.getenv("SALESFORCE_API_VERSION", "v52.0")
        self.export_query = os.getenv("SALESFORCE_EXPORT_QUERY", "SELECT Id, Name, Type, Industry, Rating FROM Account")
        self.export_interval = int(os.getenv("EXPORT_INTERVAL", 3600))  # in seconds
        self.num_records = int(os.getenv("NUM_RECORDS", 500))

