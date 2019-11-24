import requests
from bs4 import BeautifulSoup

def webScraping(url): #pass in the url of yahoo finance as a string
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    data = [ ]

    table = soup.find('table')
    tableBody = table.find('tbody')

    rows = tableBody.find_all('tr') #separate each stock into its own row
    for row in rows:
        infoDict = dict()
        information = row.findAll('td') #information for each stock

        #assign each information for each stock
        symbol = information[0].findAll(text=True)
        infoDict['symbol'] = symbol[0]

        stockName = information[1].findAll(text=True)
        infoDict['name'] = stockName[0]

        lastPrice = information[2].findAll(text=True)
        infoDict['last price'] = lastPrice[0]

        marketTime = information[3].findAll(text=True)
        infoDict['market time'] = marketTime[0]

        change = information[4].findAll(text=True)
        infoDict['change'] = change[0]

        percentChange = information[5].findAll(text=True)
        infoDict['percent change'] = percentChange[0]

        volume = information[6].findAll(text=True)
        infoDict['volume'] = volume[0]

        avgVolume3Months = information[7].findAll(text=True)
        infoDict['average volume (3 months)'] = avgVolume3Months[0]

        marketCap = information[8].findAll(text=True)
        infoDict['market capacity'] = marketCap[0]
        
        #append to the overall list
        data.append(infoDict)

    return data

# trending stock: 'https://finance.yahoo.com/trending-tickers'