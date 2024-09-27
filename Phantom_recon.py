import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Function to fetch and parse a webpage
def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to scrape from a specific site (e.g., Offensive Security blog)
def scrape_offsec_blog():
    url = 'https://www.offensive-security.com/blog/'
    soup = fetch_webpage(url)
    if soup:
        articles = []
        for article in soup.find_all('article'):
            title = article.find('h2').text.strip()
            link = article.find('a')['href']
            date = article.find('time').text.strip()
            articles.append({'Title': title, 'Link': link, 'Date': date})
        return articles
    return []

# Function to scrape from Hack The Box news
def scrape_htb_news():
    url = 'https://www.hackthebox.com/news'
    soup = fetch_webpage(url)
    if soup:
        news = []
        for item in soup.find_all('div', class_='news-item'):
            title = item.find('h3').text.strip()
            link = 'https://www.hackthebox.com' + item.find('a')['href']
            date = item.find('span', class_='date').text.strip()
            news.append({'Title': title, 'Link': link, 'Date': date})
        return news
    return []

# Function to scrape forum posts (example: Ethical Hacking Forums)
def scrape_hacking_forum():
    url = 'https://forum.hackthebox.com/categories/ethical-hacking-discussions'
    soup = fetch_webpage(url)
    if soup:
        posts = []
        for post in soup.find_all('div', class_='discussion-title'):
            title = post.text.strip()
            link = post.find('a')['href']
            posts.append({'Title': title, 'Link': link})
        return posts
    return []

# Main function to consolidate scrapes
def run_phantom_recon():
    offsec_articles = scrape_offsec_blog()
    htb_news = scrape_htb_news()
    hacking_forum_posts = scrape_hacking_forum()

    # Combine the results into a DataFrame
    combined_data = pd.DataFrame(offsec_articles + htb_news + hacking_forum_posts)
    
    # Export to a CSV file
    combined_data.to_csv('phantom_recon_data.csv', index=False)
    print("Scraping complete. Data saved to phantom_recon_data.csv.")

# Run the scraper
if __name__ == '__main__':
    print("Starting PhantomRecon...")
    run_phantom_recon()
