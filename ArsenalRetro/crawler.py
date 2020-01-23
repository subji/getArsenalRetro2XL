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


def sayhi(bot, job):
    job.context.message.reply_text(getData())


def time(bot, update, job_queue):
    job = job_queue.run_repeating(sayhi, 600, context=update)


def main():
    updater = Updater('629033245:AAEc2De6EjxzsucAbV6OHasoMfZ2QVnLejo')
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, time, pass_job_queue=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
  main()
