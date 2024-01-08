# Web Scraping with Beautiful Soap

<https://brightdata.com/blog/web-data/how-to-scrape-reddit-python> – Selenium
<https://realpython.com/beautiful-soup-web-scraper-python/> – Beautiful Soup
<https://scott-dallman.medium.com/web-scraping-dynamic-content-only-using-beautiful-soup-631496473c0e> – Scraping Dynamic Content with Beautiful Soup

To access Reddit with valid headers using Beautiful Soup, you need to pass a `User-Agent` in your headers. Reddit requires this to process your request. Here's how you can do it:

```python
import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
url = 'https://www.reddit.com/r/popular/top/?t=month'

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')       # respone.content instead of response.text is recommended

# Now you can use soup to parse the HTML
```

Remember, you should replace the User-Agent string with the one that represents your actual browser.

You can find your User-Agent by visiting a website like <https://www.whatismybrowser.com/detect/what-is-my-user-agent>. This website will display your User-Agent string, which you can then copy and use in your Python script.


## Scrapy

<https://docs.scrapy.org/en/latest/intro/tutorial.html>
<https://phantombuster.com/1146996741091941/phantoms/5545416691289264/console>
<https://www.youtube.com/watch?v=d4iz2NrZVRg>
<https://scrapeops.io/app/dashboard>

```shell
pip install scrapy scrapeops-scrapy scrapeops-scrapy-proxy-sdk
```

--

--

--

## How To Run

```shell
scraper.py -p <number_of_posts> -c <category> -t <timeframe>
```

### Options:

 `-p` or `--posts` – Number of posts to scrape. Default is 10.

 `-c` or `--category` – Category of posts to scrape (`Best`, `Hot`, `New`, `Top`, `Rising`). Default is `Top`.

 `-t` or `--timeframe` – Timeframe (if acceptable) of posts to scrape. Default is `month`.


## Code Explanation

Lines 27-28: Empty a file named `report.txt` if it exists. This file will be used to store the scraped data.

```python
with open('report.txt', 'w'):
    pass
```

---
Lines 33-34: Update the with the new url to scrape.

```python
url = soup.find('faceplate-partial', {'slot': 'load-after'}).get('src')
url = f'https://www.reddit.com{url}'
```

---
Lines 72-76: If file with the same name as `file_name` doesn't exist, we can safely create final report file. Otherwise, we need to delete the existing file and create a new one.

```python
if not os.path.exists(file_name):
    os.rename('report.txt', file_name)
else:
    os.remove(file_name)
    os.rename('report.txt', file_name)
```
