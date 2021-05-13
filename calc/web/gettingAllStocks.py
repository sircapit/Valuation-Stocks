from bs4 import BeautifulSoup
import requests

# Some configuration for Resquests work and make the propely request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
}

# Getting Brazilian Stocks registered in https://fundamentus.com.br


def getBrStocks():
    apiEnterprises = requests.get(
        'https://fundamentus.com.br/detalhes.php?papel=', headers=headers).text

    soup = BeautifulSoup(apiEnterprises, 'html.parser')

    # find the element that containts the tickets
    listPapers = list(map(lambda stock: stock.a.text, soup.find_all('tr')))

    filteredOrdinary = list(
        filter(lambda paper: paper.find("3") != -1, listPapers))  # filtering to only get Ordinary tickets (XXXX3)

    return filteredOrdinary
