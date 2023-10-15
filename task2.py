import yfinance as yf
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from datetime import datetime
import time


# Function to fetch and store ICICI Bank data
def fetch_and_store_data():
    ticker = "ICICIBANK.NS"
    
    # Create a ticker instance for ICICI Bank
    icici_bank = yf.Ticker(ticker)
    
    # Get the historical data for the last 15 minutes
    historical_data = icici_bank.history(period="15m")
    
    # Store the data in MongoDB
    store_data_in_mongodb(historical_data)

# Function to store data in MongoDB
def store_data_in_mongodb(data):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["stock_data_db"]
    collection = db["icici_bank"]

    for index, row in data.iterrows():
        # Convert the index (which is a Pandas Timestamp) to a Python datetime object
        timestamp = index.to_pydatetime()

        # Create a document to store in the MongoDB collection
        document = {
            "Timestamp": timestamp,
            "Open": row["Open"],
            "High": row["High"],
            "Low": row["Low"],
            "Close": row["Close"],
            "Volume": row["Volume"]
        }

        # Insert the document into the collection
        collection.insert_one(document)


# Create a scheduler to fetch data every 15 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_data, 'interval', minutes=15, start_date='2023-10-10 11:15:00')

# Start the scheduler
scheduler.start()

try:
    # Keep the script running to continue fetching data
    while True:
        time.sleep(5)
except (KeyboardInterrupt, SystemExit):
    # Shutdown the scheduler if the script is interrupted
    scheduler.shutdown()
