# %%
import praw
import requests
import statistics as s
import re
import pandas as pd
from time import time as t
# Reddit API requires initialization with key parameters
# before scraping
def initialization():
    ''' Define a function that initializes a subreddit object

    Parameters: None

    Returns: A subreddit object
    '''
    reddit=praw.Reddit(
        client_id="",
        client_secret="",
        user_agent="",
    )
    # From the reddit object traverse to the following subreddit
    subreddit=reddit.subreddit("guessmybf")
    return subreddit

# Define a function that scrapes the subreddit
def bf_scraper(subreddit, Num_Sub=10):
    ''' Declares a variable that dictates how many submissions to scrape

     Parameters:

     argument1 : subreddit object   
     argument2 (int) : Number of submissions the scaper collects

     Returns: The time taken to collect the data
     '''
     
    # Create a pandas dataframe to collect all the data
    df = pd.DataFrame()
    # Output: display name
    print(subreddit.display_name)
    # Output: subreddit title
    print(subreddit.title)
    # Output: a subreddit for discussion of ...
    print(subreddit.description)
    # Create a timer object
    t0=t()
    # Iterate through each submission in the subreddit
    for submission in subreddit.new(limit=Num_Sub):
        #Declare variables and reasign variables to None/NaN between submissions
        Gender = float('NaN')
        Height = None
        Weight = None
        Age = None
        bf = None
        bf_list = []
        #print(submission.title)
        # Output: the submission's title
        #Try to find a M or F to indicate gender and assign the gender to that string, otherwise leave Gender as NaN
        try:
            Gender = re.search(r'M{1}|F{1}', submission.title).group().upper()
            #print('Gender='+ Gender)
        except:
            Gender = 'NaN'
            #print('Gender='+ Gender)
        #Replace the title string with a string that has a consistent formatting using regex
        #All heights and weights are reformatted into a specific _’_ and __lb format, excluding cm and kg whicha are parsed seperately
        match=re.sub(r'\´\s*|\'\s*|\s*?(?i)f[a-z]*\s*','’',submission.title)
        match=re.sub(r'\s*lbs?|\s*pounds|\s*ibs?','lb',match)
        match=re.sub(r'\s*kg|\s*?k.[^k]*?s','kg',match)
        #print(match)
        # Attemt to find the heights and weights with the special characters and put them into a list along with regular numbers
        T = [s for s in re.findall(r'\d’\d*|\d+cm|\d+\.?\d+lb|\d+\.?\d+kg|\d+', match)]
        #Shorten the list to 3 elements as ideally the first 3 numbers should be the only relevant ones
        T = T[0:3]
        #print(T)
        #Iterate through the list and depending on the character found do different operations to reach a height in ft and remove the number from the list.
        for n in T:
            if n.find('’')==1:
                if n[2:] != '':
                    n1 = float(n[2:])/12
                    n0 = float(n[0])
                    n_h = round(n1 + n0,2)
                    Height=n_h
                    T.remove(n)
                else:
                    n_h = float(n[0])
                    T.remove(n)
            if n.find('cm') == 3:
                n_h = round(((float(n[0:3]))/30.48),2)
                Height = n_h
                T.remove(n)

        #print(T)
        #Iterate through the list but this time attempting to find a weight.
        for W in T:
            if W.find('lb')>=0:
                n_w = float(W[0:-2])
                Weight = round(n_w,2)
                T.remove(W)
            elif W.find('kg')>=0:
                n_w = float(W[0:-2])*2.20462
                Weight = round(n_w,2)
                T.remove(W)
        #if the last number meets the following condition it becomes the age
        try:
            if int(T[0])>10 and int(T[0])<55 and Height!='null' and Weight!='null':
                Age = int(T[0])
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
                'Age' : Age,
                'Gender' : Gender,
                'Height(ft)' : Height,
                'Weight(lbs)' : Weight,
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
    return(print(time))
# %%

# %%

# %%
