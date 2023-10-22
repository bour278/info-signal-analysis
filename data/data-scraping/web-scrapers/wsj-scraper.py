import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import date, timedelta
from fake_useragent import UserAgent
import time
import random

def get_data(url, headers):
    """Get data from the specified URL using the specified headers"""
    url = 'https://www.wsj.com/news/archive/2020/08/28'

    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')

    for article in soup.select('article'):
        print(article.span.text)
        print(article.h2.text)
        print(article.p.text)
        print('-' * 80)

def daterange(start_date ,end_date):
    """Generate dates between start_date and end_date"""
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2006 ,10 ,20)
end_date = date(2006 ,10, 21)

output_dir = '../../data/raw_data/'
ip_dir = '../utilities/ip-addresses.txt'

ua = UserAgent()
user_agents = [ua.random for _ in range(100)]

with open(ip_dir, 'r') as f:
    ip_addresses = [line.strip() for line in f.readlines()]

for single_date in daterange(start_date ,end_date):
    # Generate a random delay from a Gaussian distribution
    delay = random.gauss(10.0 ,1.5)

    # Wait for the specified delay before making the next request
    time.sleep(delay)

    # Randomly select a user agent and IP address from the lists
    user_agent = random.choice(user_agents)
    ip_address = random.choice(ip_addresses)

    headers ={
    'User-Agent': user_agent,
    'X-Forwarded-For': ip_address,
    }

    date_str=single_date.strftime("%Y/%m/%d")
    url=f'https://www.wsj.com/news/archive/{date_str}/'
    get_data(url ,headers)
