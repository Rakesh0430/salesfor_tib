import os
import sys
import logging
import schedule
import time
from flask import Flask, jsonify
from threading import Thread

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from salesforce import SalesforceAPI
from data_handler import save_data_to_csv

app = Flask(__name__)

# Initialize the configuration and SalesforceAPI
config = Config()
salesforce = SalesforceAPI(config)

# Setup logging
def setup_logging():
    """Set up the logging configuration."""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        filename=os.path.join(log_dir, 'app.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

setup_logging()

@app.route('/')
def home():
    return "Salesforce Data Interaction Service"

@app.route('/insert-records', methods=['POST'])
def insert_records():
    """Insert records into Salesforce."""
    try:
        salesforce.insert_records()
        logging.info("Records inserted into Salesforce.")
        return jsonify({"status": "success", "message": "Records inserted into Salesforce"}), 200
    except Exception as e:
        logging.error(f"Error inserting records: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    """Fetch data from Salesforce."""
    try:
        salesforce_data = salesforce.fetch_data()
        output_file = save_data_to_csv(salesforce_data)
        logging.info(f"Data fetched from Salesforce and saved to {output_file}")
        return jsonify({"status": "success", "file": output_file}), 200
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def scheduled_task():
    """Task to be run every 60 seconds."""
    with app.app_context():
        fetch_data()
    logging.info("Scheduled task completed.")

def run_schedule():
    """Run the scheduler."""
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Schedule the task to run every 60 seconds
    schedule.every(60).seconds.do(scheduled_task)

    # Run the scheduler in a separate thread
    scheduler_thread = Thread(target=run_schedule)
    scheduler_thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=8000)