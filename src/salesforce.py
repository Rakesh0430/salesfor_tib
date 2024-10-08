import requests
import logging
import random

class SalesforceAPI:
    """Class to interact with Salesforce API."""
    
    def __init__(self, config):
        self.config = config
        self.access_token = None
        self.instance_url = None
        self.headers = None

    def get_access_token(self):
        """Authenticate with Salesforce and obtain access token."""
        data = {
            'grant_type': 'password',
            'client_id': self.config.client_id,
            'client_secret': self.config.client_secret,
            'username': self.config.username,
            'password': self.config.password
        }
        try:
            response = requests.post(self.config.token_url, data=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            logging.info("Successfully authenticated with Salesforce.")
            
            response_data = response.json()
            self.access_token = response_data['access_token']
            self.instance_url = response_data['instance_url']
            self.headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to authenticate: {e}")
            raise

    def insert_records(self):
        """Insert dummy records into Salesforce."""
        if not self.access_token:
            self.get_access_token()

        records = []
        for i in range(self.config.num_records):
            record = {
                "attributes": {"type": "Account"},
                'Name': f'Dummy Account {i + 1}',
                'Type': random.choice(['Prospect', 'Customer', 'Partner']),
                'Industry': random.choice(['Technology', 'Healthcare', 'Finance', 'Retail']),
                'Rating': random.choice(['Hot', 'Warm', 'Cold'])
            }
            records.append(record)

        batch_size = 200
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            composite_request = {
                "allOrNone": False,
                "records": batch
            }

            try:
                response = requests.post(
                    f'{self.instance_url}/services/data/{self.config.api_version}/composite/sobjects',
                    headers=self.headers,
                    json=composite_request
                )
                response.raise_for_status()
                logging.info(f"Successfully inserted batch of {len(batch)} records")
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to insert batch: {e}")

    def fetch_data(self):
        """Fetch data from Salesforce using the configured SOQL query."""
        if not self.access_token:
            self.get_access_token()

        query_url = f'{self.instance_url}/services/data/{self.config.api_version}/query/?q={self.config.export_query}'
        try:
            response = requests.get(query_url, headers=self.headers)
            response.raise_for_status()
            logging.info("Successfully fetched data from Salesforce.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch data: {e}")
            raise
