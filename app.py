# import os
# from flask import Flask, render_template, request
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# import time

# app = Flask(__name__)

# # Function to scrape Amazon, Flipkart, and eBay for cheapest products
# def scrape_amazon(query):
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#     search_url = f"https://www.amazon.in/s?k={query}"
#     driver.get(search_url)
#     time.sleep(3)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     driver.quit()

#     products = []
#     for item in soup.select('.s-main-slot .s-result-item'):
#         name = item.select_one('h2 a span')
#         price = item.select_one('.a-price-whole')
#         link = item.select_one('h2 a')
#         if name and price and link:
#             products.append({
#                 'name': name.text,
#                 'price': price.text,
#                 'link': "https://www.amazon.in" + link['href'],
#                 'source': 'Amazon'
#             })
#     return products[:10]  # Return top 10 cheapest products


# def scrape_ebay(query):
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#     search_url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
#     driver.get(search_url)
#     time.sleep(3)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     driver.quit()

#     products = []
#     for item in soup.select('.s-item'):
#         name = item.select_one('.s-item__title')
#         price = item.select_one('.s-item__price')
#         link = item.select_one('.s-item__link')
#         if name and price and link:
#             products.append({
#                 'name': name.text,
#                 'price': price.text.replace('$', '').replace(',', ''),
#                 'link': link['href'],
#                 'source': 'eBay'
#             })
#     return products[:10]  # Return top 10 cheapest products

# def scrape_flipkart(query):
#     driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#     search_url = f"https://www.flipkart.com/search?q={query}"
#     driver.get(search_url)
#     time.sleep(3)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     driver.quit()

#     products = []
#     for item in soup.select('._1AtVbE'):
#         name = item.select_one('._4rR01T')
#         price = item.select_one('._30jeq3')
#         link = item.select_one('a._1fQZEK')
#         if name and price and link:
#             products.append({
#                 'name': name.text,
#                 'price': price.text.replace('₹', '').replace(',', ''),
#                 'link': "https://www.flipkart.com" + link['href'],
#                 'source': 'Flipkart'
#             })
#     return products[:10]  # Return top 10 cheapest products



# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/scrape', methods=['POST'])
# def scrape():
#     query = request.form['query']
#     amazon_products = scrape_amazon(query)
#     flipkart_products = scrape_flipkart(query)
#     ebay_products = scrape_ebay(query)

#     all_products = amazon_products + flipkart_products + ebay_products
#     # Sort products by price
#     all_products = sorted(all_products, key=lambda x: float(x['price'].replace(',', '')))

#     return render_template('index.html', products=all_products[:10])  # Return top 10 cheapest products across all sources

# if __name__ == '__main__':
#     # Determine if running in a hosted environment or locally
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)

import os
from flask import Flask, render_template, request
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to scrape Amazon, Flipkart, and eBay for cheapest products
def scrape_amazon(query):
    products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch headless browser
        page = browser.new_page()
        search_url = f"https://www.amazon.in/s?k={query}"
        page.goto(search_url)
        page.wait_for_timeout(3000)  # Wait for 3 seconds to load page
        soup = BeautifulSoup(page.content(), 'html.parser')

        for item in soup.select('.s-main-slot .s-result-item'):
            name = item.select_one('h2 a span')
            price = item.select_one('.a-price-whole')
            link = item.select_one('h2 a')
            if name and price and link:
                products.append({
                    'name': name.text,
                    'price': price.text,
                    'link': "https://www.amazon.in" + link['href'],
                    'source': 'Amazon'
                })
        browser.close()
    return products[:10]  # Return top 10 cheapest products


def scrape_ebay(query):
    products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch headless browser
        page = browser.new_page()
        search_url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
        page.goto(search_url)
        page.wait_for_timeout(3000)  # Wait for 3 seconds to load page
        soup = BeautifulSoup(page.content(), 'html.parser')

        for item in soup.select('.s-item'):
            name = item.select_one('.s-item__title')
            price = item.select_one('.s-item__price')
            link = item.select_one('.s-item__link')
            if name and price and link:
                products.append({
                    'name': name.text,
                    'price': price.text.replace('$', '').replace(',', ''),
                    'link': link['href'],
                    'source': 'eBay'
                })
        browser.close()
    return products[:10]  # Return top 10 cheapest products


def scrape_flipkart(query):
    products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch headless browser
        page = browser.new_page()
        search_url = f"https://www.flipkart.com/search?q={query}"
        page.goto(search_url)
        page.wait_for_timeout(3000)  # Wait for 3 seconds to load page
        soup = BeautifulSoup(page.content(), 'html.parser')

        for item in soup.select('._1AtVbE'):
            name = item.select_one('._4rR01T')
            price = item.select_one('._30jeq3')
            link = item.select_one('a._1fQZEK')
            if name and price and link:
                products.append({
                    'name': name.text,
                    'price': price.text.replace('₹', '').replace(',', ''),
                    'link': "https://www.flipkart.com" + link['href'],
                    'source': 'Flipkart'
                })
        browser.close()
    return products[:10]  # Return top 10 cheapest products


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    query = request.form['query']
    amazon_products = scrape_amazon(query)
    flipkart_products = scrape_flipkart(query)
    ebay_products = scrape_ebay(query)

    all_products = amazon_products + flipkart_products + ebay_products
    # Sort products by price
    all_products = sorted(all_products, key=lambda x: float(x['price'].replace(',', '')))

    return render_template('index.html', products=all_products[:10])  # Return top 10 cheapest products across all sources


if __name__ == '__main__':
    # Determine if running in a hosted environment or locally
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
