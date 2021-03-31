# Guess my body fat scraper

This project involves scraping data using the PRAW API to determine the bodyfats of users from their pictures. The data is scraped from the "guessmybf" subreddit and uploaded to Amazon's S3 cloud storage service using boto3. Storing the data in a data lake is more reasonable than in a data warehouse as multiple different data types are scraped including image .jpg files. From the subreddit: the age, gender, name, submission id, bodyfat and URL of the picture are stored in a csv file.

The age, gender, name, height and weight for each submission are scraped directly from the title where possible. In the following picture one can see how the titles in the subreddit are meant to store all the relevant features.

![gmbf](https://user-images.githubusercontent.com/79870177/112514713-7f43ff80-8d8d-11eb-8504-eb878afc859e.jpg)

The body fat percentage labels are found within the comments themeselves, and an average is found between all the comment's body fat predictions. An example of a comment that would be used to predict the previous users body fat is as follows.

![comment](https://user-images.githubusercontent.com/79870177/112514725-823ef000-8d8d-11eb-8541-e741a444e9ac.jpg)

As a result this project may not provide a scientific correct prediction to one's bodyfat but more of a general estimate, or perhaps an insight into how members of this subreddit percieve others body fat percentage levels.

Within the main scraping method, any urls taken from the PRAW API which are not direct urls to a jpg file are investigated further using the requests module to otain a direct jpg url. Another method can be used to naviagate through all the urls once they are stored into a csv in ordert so save them locally as jpg files within a folder. The name of the files are taken from the submission id of their respective posts.

Once the data is parsed into a csv format, it is then cleaned. Duplicates are removed from the data and sanity checks passed to ensure that numeric values are consistent with what is feasibly possible. One of the biggest challenges in handling this data is that the data is parsed directly from string written by other users. Therefore the margin for collecting data riddled with errors is much higher. To attempt to circumvent this, I used regex expressions that were as stringent as possible without completely neglecting all the data. Rows with missing values were dropped and the data set went from roughly 1000 data points to 400. Approximately 25% of weight data is missing, whereas 22% of height data is missing. In order to leverage more data in the future, ML techniques can be used to impute some of the data. Additionally, more submissions are posted each day, so as time goes on the dataset will grow.

Using the scraped data, this project aims to predict the body fat percentage of an individual given their height, weight, gender, age and a picture.
