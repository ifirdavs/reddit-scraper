import requests, os
from bs4 import BeautifulSoup
import logging
import datetime
import uuid

logging.basicConfig(filename='reddit.log', level=logging.INFO)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

distances = [4,33,62,91]
counter = 0

for d in distances:
    url = f'https://www.reddit.com/svc/shreddit/feeds/popular-feed?after=dDNfMTdqdmc1Mw%3D%3D&distance={d}&sort=TOP&t=MONTH'
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    posts = soup.find_all('shreddit-post')
    for post in posts:
        try:
            post_id = uuid.uuid1().hex
            post_url = 'https://www.reddit.com{}'.format(post.get('permalink'))
            username = post.get('author')

            user_page_url = 'https://www.reddit.com/user/{}/'.format(username)
            user_page = BeautifulSoup(requests.get(user_page_url, headers=headers).content, 'html.parser')
            
            karma = user_page.find_all('span', {'data-testid': 'karma-number'})
            post_karma, comment_karma = map(lambda x: int(x.text.replace(',','').strip()), karma)
            user_karma = post_karma + comment_karma
            user_cake_day = user_page.find('time').text.strip()

            post_category = post.get('subreddit-prefixed-name')
            post_date = post.get('created-timestamp')
            num_comments = post.get('comment-count')
            num_votes = post.get('score')
            with open('report.txt', 'a') as f:
                f.write('{};{};{};{};{};{};{};{};{};{};{}\n'.format(post_id, post_url, username, user_karma, user_cake_day, post_karma, comment_karma, post_date, num_comments, num_votes, post_category))
            counter += 1
            logging.info('Post {} successfully scraped'.format(counter))

        except Exception as e:
            counter += 1
            logging.error(f'{datetime.datetime.now()} Error scraping post {user_page_url}: {e}')
        
        if counter == 100:
            break


file_name = 'reddit-{}.txt'.format(datetime.datetime.now().strftime('%Y%m%d%H%M'))

if not os.path.exists(file_name):
    os.rename('report.txt', file_name)
else:
    os.remove(file_name)
    os.rename('report.txt', file_name)