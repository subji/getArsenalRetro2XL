from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from bs4 import BeautifulSoup
import requests
import logging

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def getData ():
  source = requests.get(
      'https://shop.adidas.co.kr/PF020401.action?PROD_CD=GE4787').text

  soup = BeautifulSoup(source, 'html.parser')
  select = soup.select('#option_selview.select_size > ul > li')
  find = soup.findAll('li', attrs={'data-option-value': True})

  for f in find:
    if f.text == '2XL' and f.get('data-size-count') is not None:
      return '아디다스 레트로 2XL 입고! ' + f.get('data-size-count') + '개 남음!'
    else:
      return '아디다스 레트로 2XL 입고 아직 안됨...'

def setTelegramBot ():
  updater = Updater(
      token='629033245:AAEc2De6EjxzsucAbV6OHasoMfZ2QVnLejo', use_context=True)
  dispatcher = updater.dispatcher
  start_handler = CommandHandler('start', sendMessage)
  dispatcher.add_handler(start_handler)
  updater.start_polling()

  echo_handler = MessageHandler(Filters.text, echo)
  dispatcher.add_handler(echo_handler)

def sendMessage (update, context):
  context.bot.send_message(
      chat_id=update.effective_chat.id, text=getData())

def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == '__main__':
  setTelegramBot()
