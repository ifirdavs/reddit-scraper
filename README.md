# Web Scraping with Beautiful Soap

<https://brightdata.com/blog/web-data/how-to-scrape-reddit-python> – Selenium
<https://realpython.com/beautiful-soup-web-scraper-python/> – Beautiful Soup

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
