import requests
from bs4 import BeautifulSoup

def createData():
    stocks = ['aapl', 'ibm', 'tsla', 'amzn', 'fb', 'nflx']
    data = []
    webPages = []
    for stock in stocks:
        webPages.append('https://s.tradingview.com/embed-widget/symbol-info/investopedia/?locale=en&symbol=' + stock + '#%7B%22symbol%22%3A%22FB%22%2C%22width%22%3A%22100%25%22%2C%22colorTheme%22%3A%22light%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A204%2C%22utm_source%22%3A%22www.investopedia.com%22%2C%22utm_medium%22%3A%22widget%22%2C%22utm_campaign%22%3A%22symbol-info%22%7D')
    #print(webPages)
    for web in webPages:
        webScraping(web)

def webScraping(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    outer = soup.find(class_='tv-embed-widget-wrapper').find(class_='tv-embed-widget-wrapper__body js-embed-widget-body').find(class_='tv-category-header tv-category-header--transparent tv-symbol-info-widget').find(class_='tv-symbol-info-widget__content js-widget-content')
    name = outer.find(class_='tv-category-header__title-line tv-symbol-info-widget__title-line').find(class_='tv-category-header__title').find(class_='tv-symbol-header__text-group tv-symbol-header__text-group--adaptive-phone').find(class_='tv-symbol-header__long-title tv-symbol-info-widget__name tv-symbol-info-widget__name--long tv-symbol-info-widget__name--adaptive').get_text()
    
    span = outer.find(class_='tv-category-header__price-line js-header-symbol-quotes').find(class_='tv-category-header__main-price js-scroll-container').find(class_='tv-scroll-wrap tv-scroll-wrap--horizontal js-scroll-scrollable-element').find(class_='tv-category-header__main-price-content').find(class_='tv-symbol-price-quote js-last-price-block i-invisible').find(class_='tv-symbol-price-quote__row js-last-price-block-value-row')#.find(class_='tv-symbol-price-quote__value js-symbol-last').find('<span>')
    print(span.findChildren())
webScraping('https://s.tradingview.com/embed-widget/symbol-info/investopedia/?locale=en&symbol=FB#%7B%22symbol%22%3A%22FB%22%2C%22width%22%3A%22100%25%22%2C%22colorTheme%22%3A%22light%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A204%2C%22utm_source%22%3A%22www.investopedia.com%22%2C%22utm_medium%22%3A%22widget%22%2C%22utm_campaign%22%3A%22symbol-info%22%7D')
#reateData()


'''
    frame = soup.find(class_='tv-embed-widget-wrapper') #.find(class_='tv-embed-widget-wrapper__body js-embed-widget-body tv-embed-widget-wrapper__body--no-border').find(class_='tv-category-header tv-category-header--transparent tv-symbol-info-widget').find(class_='tv-symbol-info-widget__content js-widget-content')
    print(frame)

    #name = frame.find(class_='tv-category-header__title-line tv-symbol-info-widget__title-line').find(class_='tv-category-header__title').find(class_='tv-symbol-header__text-group tv-symbol-header__text-group--adaptive-phone').find(class_='tv-symbol-header__long-title tv-symbol-info-widget__name tv-symbol-info-widget__name--long tv-symbol-info-widget__name--adaptive').get_text()
    #print(name)


    outerBody = soup.find(class_='comp has-right-rail l-container quote mntl-block').find(class_='comp tradingview-symbol-info').find(class_='tradingview-widget-container')

'''