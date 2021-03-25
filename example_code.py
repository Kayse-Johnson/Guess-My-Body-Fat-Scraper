from reddit_scraper import Reddit_scraper

if __name__ == '__main__':
    #Example code used to initialise the class and scrape data from
    #the guess my bf subreddit

    bf = Reddit_scraper('guessmybf')
    bf.bf_scraper(100)
    bf.cleaning()
    bf.upload('name of bucket')
