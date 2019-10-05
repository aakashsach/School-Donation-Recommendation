#Importing libraries to be used
import pandas as pd
import os
import numpy as np

#Changing the current directory
os.chdir('G:\ADV DATABASE PROJECT\io')

def main():    
    #Read the csv files into pandas dataframe    
    projects = pd.read_csv('Projects.csv')
    donations = pd.read_csv('Donations.csv')
    #Create a new dataframe with few columns of donations
    donations_proj = pd.DataFrame(donations, columns=['Project ID','Donation ID','Donor ID',])
    
    #Add donation amounnt column to the dataframe, this is done separately to avoid chances of getting nan values
    donations_proj['Donation Amount']=donations['Donation Amount']
    #Create a new dataframe with few columns of projects
    proj_part = pd.DataFrame(projects, columns=["Project ID","Project Resource Category"])
    #Join the temp and tempproj dataframes using left join on Project ID
    final_op = pd.merge(donations_proj,proj_part, on='Project ID', how='left')
    #Create a new dataframe by grouping Donor ID and Project Resource Category and also get the sum and count of Donation Amount
    donorStats=final_op.groupby(['Donor ID','Project Resource Category'])[['Donation Amount']].agg(['sum','count'])
    donorStats.head()
    #Split the final dataframe into 20 dataframes to write them into csv using numpy library in python
    finalop_split=np.array_split(donorStats,20)
    #Write the 20 divided datafrmaes to csvs using pipeline as separator
    finalop_split[0].to_csv('DonorStats1.csv')
    finalop_split[1].to_csv('DonorStats2.csv')
    finalop_split[2].to_csv('DonorStats3.csv')
    finalop_split[3].to_csv('DonorStats4.csv')
    finalop_split[4].to_csv('DonorStats5.csv')
    finalop_split[5].to_csv('DonorStats6.csv')
    finalop_split[6].to_csv('DonorStats7.csv')
    finalop_split[7].to_csv('DonorStats8.csv')
    finalop_split[8].to_csv('DonorStats9.csv')
    finalop_split[9].to_csv('DonorStats10.csv')
    finalop_split[10].to_csv('DonorStats11.csv')
    finalop_split[11].to_csv('DonorStats12.csv')
    finalop_split[12].to_csv('DonorStats13.csv')
    finalop_split[13].to_csv('DonorStats14.csv')
    finalop_split[14].to_csv('DonorStats15.csv')
    finalop_split[15].to_csv('DonorStats16.csv')
    finalop_split[16].to_csv('DonorStats17.csv')
    finalop_split[17].to_csv('DonorStats18.csv')
    finalop_split[18].to_csv('DonorStats19.csv')
    finalop_split[19].to_csv('DonorStats20.csv')


if __name__ == '__main__':
    main()    