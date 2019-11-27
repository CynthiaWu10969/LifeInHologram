import requests
from bs4 import BeautifulSoup

def scraping(url='https://finance.yahoo.com/most-active?count=25&offset=0'): #pass in the url of yahoo finance as a string
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
        infoDict['Symbol'] = symbol[0]

        stockName = information[1].findAll(text=True)
        infoDict['Name'] = stockName[0]

        lastPrice = information[2].findAll(text=True)
        infoDict['Price'] = lastPrice[0]

        marketTime = information[3].findAll(text=True)
        infoDict['Change'] = marketTime[0]

        change = information[4].findAll(text=True)
        infoDict['% Change'] = change[0]

        percentChange = information[5].findAll(text=True)
        infoDict['Volume'] = percentChange[0]

        volume = information[6].findAll(text=True)
        infoDict['avg volume'] = volume[0]

        avgVolume3Months = information[7].findAll(text=True)
        infoDict['Market Cap'] = avgVolume3Months[0]
        
        #append to the overall list
        data.append(infoDict)

    return data[:6]#

print(scraping('https://finance.yahoo.com/most-active?count=25&offset=0'))