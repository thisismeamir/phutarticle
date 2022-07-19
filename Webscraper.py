from cgitb import text
import requests
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from templates import arxiveTemplate as aT


class webscraper:
    def __init__(self, url='') -> None:
        self.url = url
        if 'arxiv' in self.url:
            scraped  = self.request()
            if scraped != 'NF':
                scraped = self.arxivscraper()
                if scraped == 0:
                  self.output =  aT([self.Title,self.url,self.Abstract,self.Date,self.Authors,self.Subject])
            else:
                pass
        else:
            pass

    def request(self):
        url = self.url
        if  requests.get(url).ok:
            session = HTMLSession()
            self.response = session.get(self.url)
        else:
            return 'NF'

    def arxivscraper(self):
        soup = bs(self.response.content, 'html.parser')
        self.Title = soup.find('h1', class_='title mathjax').text
        self.Date  = soup.find('div',calss_='dateline')
        self.Authors = soup.find('div', class_='authors').find_all('a')

        # Authors scraping
        cleanAuths = []
        for auth in self.Authors:
            auth = auth.text
            cleanAuths.append(auth)
        self.Authors = cleanAuths

        self.Abstract  = soup.find('div', id='abs').find_all('blockquote')

        #Abstract scraping
        cleanAbs = []
        for ab in self.Abstract:
            ab = ab.text
            cleanAbs.append(ab)
        self.Abstract = cleanAbs
        self.Subject = soup.find('span', class_='primary-subject').text
        return 0  

