# The bot main python file
# coding:utf-8
import telebot
from telebot import formatting
from Webscraper import webscraper as ws
import os
from cgitb import text
import requests
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession


class webscraper:
     def __init__(self, url='') -> None:
          self.url = url
          if 'arxiv' in self.url:
               scraped  = self.request()
               if scraped != 'NF':
                    scraped = self.arxivscraper()
                    if scraped == 0:
                         self.output =  webscraper.arxiveTemplate([self.Title,self.url,self.Abstract,self.Date,self.Authors,self.Subject])
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
     @staticmethod
     def arxiveTemplate(src = list):
          auth = ""
          for i in src[4]:
               auth = i + ", "
          auth = auth[0:-2]
          src[2][0] = src[2][0].replace('\n','')
          text = f"""
          📄 {src[0][6:]} \n {src[1]}\n\n 🔵 Abstract:{src[2][0][9:]}\n \n 📌 {src[5]}\n 👤 {auth} \n\n ----\n @UTPhysicsArticles
          """
          text = u"{0}".format(text)
          return text


PORT = int(os.environ.get('PORT', 5000))

#----- API KEY importing -----

botAPI = '5428798399:AAH89nqubHm378fQicd1dgTgk7uSAFgIoB8'
bot = telebot.TeleBot(botAPI)

def Truepasser(message):
     return True
#----- BOT body -----
def main():
     # Bot basic commands
     @bot.message_handler(commands=['start'])
     def start(message):
          bot.reply_to(message, f"I am ready! \n hit me with an arxiv link or a youtube link, also I am able to work with DOI links.")

     @bot.message_handler(commands=['About'])
     def start(message):
          bot.reply_to(message, "I am an assitant to make posts for @UTPhysicsArticles faster!")

     
     @bot.message_handler()
     def Linksend(message):
          text = message.text
          answer = ws(text)
          abstract = answer.Abstract[0][9:].replace("\n","")
          title = answer.Title[6:]
          auth = ""
          for i in answer.Authors:
               auth = i + ", "
          auth = auth[0:-2]
          
          bot.send_message(chat_id = -1001183234135, text=formatting.format_text(formatting.hbold(f"📄 {title}\n"),formatting.hitalic(answer.url),formatting.hpre("\n\n"),formatting.hbold(f"🔵 Abstract:"),formatting.hitalic(abstract),formatting.hpre("\n\n"),formatting.hbold(f'📌 {answer.Subject}\n'),formatting.hitalic(auth),separator=" "),parse_mode='HTML' )
         
     bot.polling()
     
if __name__ == '__main__':
     main()

