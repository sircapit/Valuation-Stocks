from bs4 import BeautifulSoup
import requests
import concurrent.futures
from math import sqrt
from web.gettingAllStocks import getBrStocks

# Some configuration for Resquests work and make the propely request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
}

stocks = getBrStocks()

cheapStocks = {}

# Checking each stock's VPA and LPA and apply Graham Formula to see if it's cheap


def filtering(paper):
    linkForStock = f"https://fundamentus.com.br/detalhes.php?papel={paper}"

    stockSite = requests.get(linkForStock, headers=headers).text

    stockSoup = BeautifulSoup(stockSite, 'html.parser')

    try:
        LPA, _, VPA, * \
            g = stockSoup.div.find_all('td', class_='data w2')[2:]
        # Getting LPA and VPA and converting them to float
        LPA, VPA = float(LPA.span.text.replace(',', '.')), float(
            VPA.span.text.replace(',', '.')),

        if (LPA < 0.0) or (VPA < 0.0):
            # Negative values should be avoided (I want distance from stocks like that (LPA or VPA < 0))
            pass
        else:
            formula = sqrt(LPA*VPA*22.5)

            actualPrice = float(stockSoup.div.find(
                'td', class_='data destaque w3').span.text.replace(',', '.'))

            if (actualPrice < formula):
                print(paper, actualPrice, formula)
                cheapStocks[paper] = actualPrice
            else:
                pass

    # There're some stocks that didn't send their VPA and LPA, so let's skip those ones.
    except ValueError:
        pass


with concurrent.futures.ThreadPoolExecutor() as executor:
    # Basic threading. Just to speed up the process.
    executor.map(filtering, stocks)

# Final Result: A dictionary with a cheap stock's ticket (as key) and its price (as value)
print(cheapStocks)
