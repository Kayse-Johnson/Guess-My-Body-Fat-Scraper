from body_fat_reddit_scrape import initialization, bf_scraper
from Clean_bf_data import cleaning
subreddit = initialization()
bf_scraper(subreddit,5)
cleaning()
