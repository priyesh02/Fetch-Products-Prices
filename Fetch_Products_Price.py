import pandas as pd
import numpy as np
import os
from datetime import datetime
import schedule
import time
import requests
from bs4 import BeautifulSoup
import schedule


# Address of file having Product Name, Website Name,  URL
product_details = pd.read_excel("D:/Python/Projects/Product Price Comparision/Product_links.xlsx")


# Function to fetch product prices from different websites

def fetch_prices():
    # Read data from Excel file
    df_input = pd.read_excel(
        "D:/Python/Projects/Product Price Comparision/Product_links.xlsx")  # Replace 'products.xlsx' with your Excel file path

    # Initialize a dictionary to hold data
    data = {'date': [], 'website': [], 'product_name': [], 'price': []}

    # Current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Iterate through each row in the Excel file
    for index, row in df_input.iterrows():
        url = row['Product_link']
        website = row['Website_name']
        product_name = row['Product_Name']

        # Fetch the webpage content
        headers = {
            'User-Agent': 'https://explore.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Locate the price element

        if website == "amazon":
            price_element = soup.find("span", attrs={'class': 'a-price-whole'})

        else:
            price_element = soup.find("div", attrs={'class': 'Nx9bqj CxhGGd'})

        if price_element:
            price = price_element.get_text()
            price = price.replace("₹", "").strip()
            price = price.replace(",", "").strip()
            price = float(price)
            # Store the data
            data['date'].append(current_date)
            data['website'].append(website)
            data['product_name'].append(product_name)
            data['price'].append(price)

    # Convert data to pandas DataFrame
    df_output = pd.DataFrame(data)

    # Specify the CSV file path
    csv_file_path = "D:/Python/Projects/Product Price Comparision/Product_Prices.csv"

    # Check if the file already exists
    file_exists = os.path.exists(csv_file_path)

    # Determine whether to include headers
    include_header = not file_exists  # True if file doesn't exist, False if it does

    # Append data to CSV file
    df_output.to_csv(csv_file_path, mode='a', header=include_header, index=False)

    print(f"Data recorded for {current_date}")


fetch_prices()


# !!! Run below Script to keep it continuously tracking Price everyday.

schedule.every().day.at('09:00').do(fetch_prices)  # Adjust the time as needed

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute