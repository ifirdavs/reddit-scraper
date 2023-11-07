import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import logging
import datetime
import uuid
import time


logging.basicConfig(filename='reddit.log', level=logging.INFO)

url = 'https://www.reddit.com/r/popular/top?t=month/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

now = datetime.datetime.now()
file_name = 'reddit-{}.txt'.format(now.strftime('%Y%m%d%H%M'))

with open(file_name, 'w') as f:
    f.write('UNIQUE_ID;post URL;username;user karma;user cake day;post karma;comment karma;post date;number of comments;number of votes;post category\n')

counter = 0

# Scroll to load more posts
driver = webdriver.Chrome()
driver.get(url)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)


soup = BeautifulSoup(driver.page_source, 'html.parser')
posts = soup.find_all('shreddit-post')
for post in posts:
    try:
        post_id = uuid.uuid1().hex
        post_url = 'https://www.reddit.com{}'.format(post.get('permalink'))
        username = post.get('author')

        user_page_url = 'https://www.reddit.com/user/{}/'.format(username)
        user_page = BeautifulSoup(requests.get(user_page_url, headers=headers).content, 'html.parser')
        
        karma = user_page.find_all('span', {'data-testid': 'karma-number'})
        post_karma, comment_karma = map(lambda x: int(x.text.replace(',','').strip('\n')), karma)
        user_karma = post_karma + comment_karma
        user_cake_day = user_page.find('faceplate-date').get('ts')
        

        post_category = post.get('subreddit-prefixed-name')
        post_date = post.get('created-timestamp')
        num_comments = post.get('comment-count')
        num_votes = post.get('score')
        with open(file_name, 'a') as f:
            f.write('{};{};{};{};{};{};{};{};{};{};{}\n'.format(post_id, post_url, username, user_karma, user_cake_day, post_karma, comment_karma, post_date, num_comments, num_votes, post_category))
        counter += 1
        logging.info('Post {} successfully scraped'.format(counter))

    except Exception as e:
        counter += 1
        logging.error(f'{now} Error scraping post {counter}: {e}')
    
    if counter == 6:
        driver.quit()
        break
