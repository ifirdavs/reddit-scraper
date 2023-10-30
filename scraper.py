import requests
from bs4 import BeautifulSoup
import logging
import datetime


logging.basicConfig(filename='reddit.log', level=logging.INFO)

url = 'https://www.reddit.com/r/popular/top/?t=month'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

now = datetime.datetime.now()
file_name = 'reddit-{}.txt'.format(now.strftime('%Y%m%d%H%M'))
