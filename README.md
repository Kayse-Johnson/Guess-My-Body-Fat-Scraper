# Guess my body fat scraper

This project involves scraping data using the PRAW API to determine the bodyfats of users from their pictures. The data is scraped from the "guessmybf" subreddit and uploaded to Amaxon's S3 cloud storage service. Storing the data in a data lake is more reasonable than in a data warehouse as multiple different data types are scraped including image .jpg files. From the subreddit: the age, gender, name, submission id, bodyfat and URL of the picture are stored in a csv file.

The age, gender, name, height and weight for each submission are scraped directly from the title where possible

![gmbf](https://user-images.githubusercontent.com/79870177/112513782-96362200-8d8c-11eb-9e7a-cf1ee6488664.jpg)

Using the scraped data, this project aims to predict the body fat percentage of an individual given their height, weight, gender, age and a picture.
