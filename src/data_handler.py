import pandas as pd
import logging
from datetime import datetime

def save_data_to_csv(salesforce_data):
    """Save Salesforce data to a CSV file."""
    try:
        records = salesforce_data['records']
        df = pd.DataFrame(records)
        
        if 'attributes' in df.columns:
            df = df.drop(columns='attributes')
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_csv_file = f'salesforce_data_{timestamp}.csv'
        df.to_csv(output_csv_file, index=False)
        logging.info(f"Data successfully saved to {output_csv_file}")
        return output_csv_file
    except Exception as e:
        logging.error(f"Failed to save data to CSV: {e}")
        raise
