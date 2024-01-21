import requests
from bs4 import BeautifulSoup
import csv
import time
import random

def amzsrch(search_query):
    amzurl = "https://www.amazon.in/s"
    params = {"k": search_query} #in this dictionary variable keyvalue passed in parameter as search query 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'} #headers are taken from stackoverflow so website wont show 503 error

    # Send a GET request to Amazon with the search query
    response = requests.get(amzurl, params=params, headers=headers)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the product details from the search results
        products = soup.find_all('div', {'data-asin': True})
        results = []

        for product in products[:100]: #I'm taking first 100 search results
            title1_element = product.find('span', {'class': 'a-color-base'})
            title1 = title1_element.get_text(strip=True) if title1_element else 'Brand not available'

            title_element = product.find('span', {'class': 'a-text-normal'})
            title = title_element.get_text(strip=True) if title_element else 'Title not available'

            price_element = product.find('span', {'class': 'a-price-whole'})
            price = price_element.get_text(strip=True) if price_element else 'Price not available'

            rating_element = product.find('span', {'class': 'a-icon-alt'})
            rating = rating_element.get_text(strip=True) if rating_element else 'Rating not available'

            results.append({'Brand': title1,'Title': title, 'Price': price, 'Rating': rating})


        return results
    else:
        print(f"Failed to fetch search results. Status code: {response.status_code}")
        return None

def save_to_csv(results, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile: #opening filein write mode so it will clear previous saved results
        fieldnames = ['Brand', 'Title', 'Price', 'Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)

def preview_csv(csv_filename):
    with open(csv_filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)

if __name__ == "__main__":
    search_query = input("Enter the search query on Amazon: ")
    csv_filename = "amazon_search_results.csv"

    results = amzsrch(search_query)

    if results:
        save_to_csv(results, csv_filename)
        print(f"\nResults saved to {csv_filename}.\n")
        print("Preview of the first few rows:")
        preview_csv(csv_filename)
    else:
        print("Failed to fetch search results. Please check your internet connection and try again.")
