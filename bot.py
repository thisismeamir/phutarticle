# The bot main python file
# coding:utf-8
import telebot
from telebot import formatting
from Webscraper import webscraper as ws

#----- API KEY importing -----

botAPI = ''
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

