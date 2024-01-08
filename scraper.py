import requests, os
from bs4 import BeautifulSoup
import logging
import datetime
import uuid
import argparse

logging.basicConfig(filename='reddit.log', level=logging.INFO)

parser = argparse.ArgumentParser(description='Scrape Reddit')

parser.add_argument('-p', '--posts', type=int, default=100, help='Number of posts')
parser.add_argument('-c', '--category', type=str, default="top", help='Category')
parser.add_argument('--period', type=str, default="month", help='Period')

args = parser.parse_args()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}

post_counter = 0
error_counter = 0

break_flag = False

url = f'https://www.reddit.com/svc/shreddit/feeds/popular-feed?sort={args.category}&t={args.period}'

with open('report.txt', 'w'):
    pass

while True:
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    posts = soup.find_all('shreddit-post')
    url = soup.find('faceplate-partial', {'slot': 'load-after'}).get('src')
    url = f'https://www.reddit.com{url}'
    
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
            post_counter += 1
            logging.info('Post {} successfully scraped'.format(post_counter))

        except Exception as e:
            logging.error(f'{datetime.datetime.now()} Error scraping post {user_page_url}: {e}')
            error_counter += 1

        if post_counter == args.posts or error_counter == 10:
            break_flag = True
            break
    if break_flag:
        break

file_name = 'reddit-{}.txt'.format(datetime.datetime.now().strftime('%Y%m%d%H%M'))

if not os.path.exists(file_name):
    os.rename('report.txt', file_name)
else:
    os.remove(file_name)
    os.rename('report.txt', file_name)