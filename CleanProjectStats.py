#Importing libraries to be used
import pandas as pd
import numpy as np
#import math
import string
import os
from collections import Counter
from nltk.corpus import stopwords

#Changing the current directory
os.chdir('G:\ADV DATABASE PROJECT\io')
#Getting the english stopwords (words that are not much important for searching)
stopwords = stopwords.words('english')

def main():
    #Read the csv files into pandas dataframe
    donations=pd.read_csv('Donations.csv')
    projects=pd.read_csv('Projects.csv')
    
    #Clean the Essays using method
    projects['Project Essay'] = projects['Project Essay'].astype(str)    
    projects['Essay']=projects['Project Essay'].apply(_clean)

    #Generate words from the cleaned essay
    projects['Words']=projects['Essay'].apply(lambda a: word_gen(a,1))

    #Get top words from each words column of essay and store them in TopWords column
    projects['TopWords']=''
    for i in range(0,projects.shape[0]):
        projects['TopWords'].iloc[i]=best_words(projects['Words'].iloc[i])
   


    #Create a new dataframe with specific columns of the projects dataframe
    projects_words = pd.DataFrame(projects, columns=["Project ID","Project Resource Category",
                                       "Project Current Status","Project Cost","TopWords"])


    #Group by Project ID from donations dataframe and store in a new dataframe
    projects_donations=donations.groupby('Project ID')
    #Aggregate the column donation amount and calculate their sum
    donation_am=projects_donations['Donation Amount'].sum()
    #Remove the header index and use column names
    donation_am=donation_am.reset_index()

    #Create a new dataframe getting Proect ID column from aggregate agg
    don_project=pd.DataFrame(donation_am,columns=['Project ID'])

    #Join the dataframes project_words and don_project using left join on Project ID
    projectStats = pd.merge(projects_words,don_project, on='Project ID', how='left')
    
    #Add the column Donation Amount from agg to 
    projectStats['Donation Amount']=donation_am['Donation Amount']
    #Get the strength of donations through donation amount and project cost
    projectStats['Weightage']=(projectStats['Donation Amount']/projectStats['Project Cost'])*100
    #Fill the null values in Donation Amount and Weightage with 0
    projectStats['Donation Amount'].fillna(0, inplace=True)
    projectStats['Weightage'].fillna(0, inplace=True)

    #Split the final dataframe into 20 dataframes to write them into csv using numpy library in python
    projectStatsSplit=np.array_split(projectStats,20)
    
    #Write the 20 divided datafrmaes to csvs using pipeline as separator
    projectStatsSplit[0].to_csv('ProjectStats1.csv',sep="|")
    projectStatsSplit[1].to_csv('ProjectStats2.csv',sep="|")
    projectStatsSplit[2].to_csv('ProjectStats3.csv',sep="|")
    projectStatsSplit[3].to_csv('ProjectStats4.csv',sep="|")
    projectStatsSplit[4].to_csv('ProjectStats5.csv',sep="|")
    projectStatsSplit[5].to_csv('ProjectStats6.csv',sep="|")
    projectStatsSplit[6].to_csv('ProjectStats7.csv',sep="|")
    projectStatsSplit[7].to_csv('ProjectStats8.csv',sep="|")
    projectStatsSplit[8].to_csv('ProjectStats9.csv',sep="|")
    projectStatsSplit[9].to_csv('ProjectStats10.csv',sep="|")
    projectStatsSplit[10].to_csv('ProjectStats11.csv',sep="|")
    projectStatsSplit[11].to_csv('ProjectStats12.csv',sep="|")
    projectStatsSplit[12].to_csv('ProjectStats13.csv',sep="|")
    projectStatsSplit[13].to_csv('ProjectStats14.csv',sep="|")
    projectStatsSplit[14].to_csv('ProjectStats15.csv',sep="|")
    projectStatsSplit[15].to_csv('ProjectStats16.csv',sep="|")
    projectStatsSplit[16].to_csv('ProjectStats17.csv',sep="|")
    projectStatsSplit[17].to_csv('ProjectStats18.csv',sep="|")
    projectStatsSplit[18].to_csv('ProjectStats19.csv',sep="|")
    projectStatsSplit[19].to_csv('ProjectStats20.csv',sep="|")
    
#Method to divide words, may be used in future to create group of words by modifying value of N (creating ngrams)    
def word_gen(txt,N):
    #words = [txt[i:i+N] for i in range(len(txt)-N+1)]
    #words = [" ".join(b) for b in words]
    return txt.split()

#Method to clean text; It converts the text to lowercase, remove punctuations and removes the words that have no importance using stopwords and other noise
def _clean(text):
    #text=text.astype(str)
    #Convert everything to lowercase
    text=text.lower()
   
    #Remove punctuations from the text using python's string.punctuation
    nopunc_txt=""
    for x in text:
        if x not in string.punctuation:
            nopunc_txt = nopunc_txt+''.join(x)
   
    clean_text=""
    #Remove the stopwords    
    for w in nopunc_txt.split():
       
        if w in stopwords:
            continue
        clean_text +=" "
        clean_text +=w
       
    noise = ['also', 'students','title', 'would', 'every', 'my', 'will', 'many', 'donotremoveessaydivider','teacher', 'subject']
    #Remove the noise
    for n in noise:
        clean_text=clean_text.replace(n,"")
       
    return clean_text

#Method to get the top words from each essay based on their count in the text using Counter in collections library of python
def best_words(words):
    all_top_words=[]
    #Get all words
    all_top_words.extend(x for x in words)
    #Apply counter and get the top 25 words along with their count
    t = Counter(all_top_words).most_common(25)
    #Retrieve the words and leave their count
    final_words=[w[0] for w in t]
    return final_words

    
if __name__ == '__main__':
    main()