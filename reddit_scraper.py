import praw
import requests
import statistics as s
import re
import pandas as pd
from time import time as t
import missingno as msno
from pprint import pprint
import boto3
class Reddit_scraper:
    def __init__(self, subreddit,bucket=None):
        '''initializes the attributes
        
        Parameters: 
        subreddit- The specific subreddit that the the scraper uses to parse data
        bucket - the bucket used to store the data

        '''
        reddit=praw.Reddit(
        client_id="In3tHnD0wHz8jQ",
        client_secret="ophvkfmAaLZTe2L8MtSkO-qjZkH9wg",
        user_agent="Kayse"
        )
        # From the reddit object traverse to the following subreddit
        self.subreddit = reddit.subreddit(subreddit)
        self.bucket = bucket

    def bf_scraper(self, Num_Sub=10):
        ''' Declares a variable that dictates how many submissions to scrape

        Parameters:

        argument1 : subreddit object   
        argument2 (int) : Number of submissions the scaper collects

        Returns: The time taken to collect the data
        '''
        
        # Create a pandas dataframe to collect all the data
        df = pd.DataFrame()
        # Output: display name
        print(self.subreddit.display_name)
        # Output: subreddit title
        print(self.subreddit.title)
        # Output: a subreddit for discussion of ...
        print(self.subreddit.description)
        # Create a timer object
        t0=t()
        # Iterate through each submission in the subreddit
        for submission in self.subreddit.new(limit=Num_Sub):
            #Declare variables and reasign variables to None/NaN between submissions
            gender = float('NaN')
            height = None
            weight = None
            age = None
            bf = None
            bf_list = []
            #print(submission.title)
            # Output: the submission's title
            #Try to find a M or F to indicate gender and assign the gender to that string, otherwise leave Gender as NaN
            try:
                gender = re.search(r'M{1}|F{1}', submission.title).group().upper()
                #print('Gender='+ Gender)
            except:
                gender = 'NaN'
                #print('Gender='+ Gender)
            #Replace the title string with a string that has a consistent formatting using regex
            #All heights and weights are reformatted into a specific _’_ and __lb format, excluding cm and kg whicha are parsed seperately
            match=re.sub(r'\´\s*|\'\s*|\s*?(?i)f[a-z]*\s*','’',submission.title)
            match=re.sub(r'\s*lbs?|\s*pounds|\s*ibs?','lb',match)
            match=re.sub(r'\s*kg|\s*?k.[^k]*?s','kg',match)
            #print(match)
            # Attemt to find the heights and weights with the special characters and put them into a list along with regular numbers
            l = [s for s in re.findall(r'\d’\d*|\d+cm|\d+\.?\d+lb|\d+\.?\d+kg|\d+', match)]
            #Shorten the list to 3 elements as ideally the first 3 numbers should be the only relevant ones
            l = l[0:3]
            #print(T)
            #Iterate through the list and depending on the character found do different operations to reach a height in ft and remove the number from the list.
            for n in l:
                if n.find('’')==1:
                    if n[2:] != '':
                        n1 = float(n[2:])/12
                        n0 = float(n[0])
                        n_h = round(n1 + n0,2)
                        height=n_h
                        l.remove(n)
                    else:
                        n_h = float(n[0])
                        l.remove(n)
                if n.find('cm') == 3:
                    n_h = round(((float(n[0:3]))/30.48),2)
                    height = n_h
                    l.remove(n)

            #print(T)
            #Iterate through the list but this time attempting to find a weight.
            for w in l:
                if w.find('lb')>=0:
                    n_w = float(w[0:-2])
                    weight = round(n_w,2)
                    l.remove(w)
                elif w.find('kg')>=0:
                    n_w = float(w[0:-2])*2.20462
                    weight = round(n_w,2)
                    l.remove(w)
            #if the last number meets the following condition it becomes the age
            try:
                if int(l[0])>10 and int(l[0])<55 and height!='null' and weight!='null':
                    age = int(l[0])
            except:
                pass

            #print(Gender)
            #print('weight =', Weight)
            #print('height =',Height)
            #print('age =', Age)
            #print(submission.score)
            # Output: the submission's score
            #print(submission.author.name)
            # Output: the submission's ID
            #print(submission.url)
            # Output: the URL the submission points to 


            #Iterate through the comments in the submission
            for top_level_comment in submission.comments:
                #print(top_level_comment.body)
                #For each comment grab all the numbers excluding ones that are not relevant for instance ones referring to weight or height
                a = [int(s) for s in re.findall(r'(?<!’)\b\d+(?!’|\d*lbs)', top_level_comment.body)]
                #Ensure all the numbers in the list are feasible bodyfat percentages then append them to a separate list
                try:
                    for number in a:
                        if number < 6 or number > 45: 
                            pass
                        else:
                            bf_list.append(number)

                # if there is no number this ensures the code continues  
                except TypeError:
                    pass
            #print(bf)
            try:
                bf = round(s.mean(bf_list),2)
            except:
                pass
            #Some submissions seem to not have names throwing errors, this allows the program to contine regardless
            try:
                data = {
                    'Name' : submission.author.name,
                    'ID' : submission.id,
                    'Age' : age,
                    'Gender' : gender,
                    'Height(ft)' : height,
                    'Weight(lbs)' : weight,
                    'bodyfat(%)' : bf,
                    'URL' : submission.url
                }
            except:
                pass
            #Append each dataframe and write to a csv file
            df = df.append(data, ignore_index= True)
            df.to_csv('Body_Fat_Reddit_Data.csv', index=False)
            t1 = t()
            #output the total time it took  to scrape the data
            time = t1-t0
            #print(bf_list)
            #print(bf)
            #print()
        print(df)
        print(time)
    
    def cleaning(self):
        ''' Recieve the dirty data file and proceed to clean it and visualise it to better understand the data
        before creating a new csv file without missing values and duplicates.
        '''

        # Set option to display more rows for better viewing
        pd.set_option('display.max_rows',100)
        #Read in the dirty csv data file
        df=pd.read_csv('Body_Fat_Reddit_Data.csv')
        #Print the number of duplicates, their rows and remove them
        print(df.duplicated().sum())
        duplicates = df.duplicated(keep=False)
        print(df[duplicates])
        df.drop_duplicates(inplace=True, ignore_index=True)
        pprint(df)
        print()
        #Describe the data set to ensure numbers are reasonable
        pprint(df.describe())
        print()
        #Remove rows that have unrealistic data
        df = df.loc[df['Height(ft)']<9]
        pprint(df)
        print()
        pprint(df.describe())
        print()
        #Determine the number of missing values as a percentage and visualise it
        null_index=df.isnull()
        pprint(null_index.mean()*100)
        print()
        #print(msno.matrix(df))
        #print()
        #Remove rows with missing values
        clean=df.dropna()
        pprint(clean)
        print()
        #Create a new csv file with the cleaned data
        clean.to_csv('Clean_Body_Fat_Reddit_Data.csv', index=False)

    def upload(self,bucket):
        '''Uploads data files to the s3 bucket
        Parameters:
        argument : the name of the bucket the data is stored in
        '''
        self.bucket = bucket
        s3 = boto3.resource('s3')
        # Print out bucket names
        for bucket in s3.buckets.all():
            print(bucket.name)
        # Upload the data files
        data = open('Body_Fat_Reddit_Data.csv', 'rb')
        s3.Bucket(self.bucket).put_object(Key='Dirty_bf.csv', Body=data)
        try:
            data = open('Clean_Body_Fat_Reddit_Data.csv', 'rb')
            s3.Bucket(self.bucket).put_object(Key='Clean_bf.csv', Body=data)
        except:
            pass
        