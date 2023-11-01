import requests
from bs4 import BeautifulSoup
import logging
import datetime
import uuid


logging.basicConfig(filename='reddit.log', level=logging.INFO)

url = 'https://www.reddit.com/r/popular/top/?t=month'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

now = datetime.datetime.now()
file_name = 'reddit-{}.txt'.format(now.strftime('%Y%m%d%H%M'))

with open(file_name, 'w') as f:
    f.write('UNIQUE_ID;post URL;username;user karma;user cake day;post karma;comment karma;post date;number of comments;number of votes;post category\n')

counter = 0

session = requests.Session()
session.headers.update(headers)

while counter < 100:
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    posts = soup.find_all('div', {'class': 'Post'})
    for post in posts:
        try:
            post_id = uuid.uuid1().hex
            post_url = 'https://www.reddit.com{}'.format(post.find('a', {'class': 'SQnoC3ObvgnGjWt90zD9Z'}).get('href'))
            username = post.find('a', {'class': '_2tbHP6ZydRpjI44J3syuqC'}).text
            user_karma = post.find('span', {'class': '_1hNyZuYYsjW8F6k7yPvlvf'}).text
            user_cake_day = post.find('span', {'class': '_3jOxDPIQ0KaOWpzvSQo-1s'}).text
            post_karma = post.find('div', {'class': '_1rZYMD_4xY3gRcSS3p8ODO'}).text
            comment_karma = post.find('span', {'class': '_2h_2_gNIYFyvKYiK9oZnqS'}).text
            post_date = post.find('a', {'class': '_3jOxDPIQ0KaOWpzvSQo-1s'}).text
            num_comments = post.find('span', {'class': '_1rZYMD_4xY3gRcSS3p8ODO'}).text
            num_votes = post.find('div', {'class': '_1rZYMD_4xY3gRcSS3p8ODO'}).text
            post_category = post.find('a', {'class': '_3ryJoIoycVkA88fy40qNJc'}).text
            with open(file_name, 'a') as f:
                f.write('{};{};{};{};{};{};{};{};{};{};{}\n'.format(post_id, post_url, username, user_karma, user_cake_day, post_karma, comment_karma, post_date, num_comments, num_votes, post_category))
            counter += 1
            logging.info('Post {} successfully scraped'.format(counter))
        except:
            logging.error('Error scraping post')

session.close()