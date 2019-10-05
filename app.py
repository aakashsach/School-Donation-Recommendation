from flask import Flask, render_template, request, jsonify, url_for
from flask_mysqldb import MySQL
from random import randint
import pandas as pd
import numpy as np
from PIL import Image
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
plt.rcdefaults()
app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'abc'
app.config['MYSQL_DB'] = 'test'
mysql = MySQL(app)

#Webpage - running
@app.route('/')
def Index():
    return render_template('index.html')

 # publish wordcloud
@app.route('/search', methods=['GET', 'POST'])
def search():
    all_top_words = []
    category = request.form['category']

    #Connect to mysql
    cur = mysql.connection.cursor()

    # TopWords column has an array of 25 words extracted from each donor essay
    # List 25 such topwords(array of 25 words) for each resource category
    query = "SELECT TopWords FROM ProjectStats WHERE ProjectResourceCategory=%s Order BY DonationStrength DESC LIMIT 25"
    
    #Pass parameter of resource category as arguement in query
    cur.execute(query, [category, ])
    data = cur.fetchall()
    cur.close()
    top_words = data

    # get all words in all_top_words
    for i in range(0, len(top_words)):
        all_top_words.extend(x for x in top_words)
    
    # Get top 40 words with their count
    t = Counter(str(all_top_words).split()).most_common(40)
    
    # Extract just the words from top 40
    final_words = [w[0] for w in t]

    #Reduce noise
    final_words = (str(final_words).replace("',", ""))

    # Use wordcloud library to generate the worcloud with required attributes
    wcloud = WordCloud(max_words=100, colormap='cool', background_color='white',
                       normalize_plurals=True).generate((str(final_words).replace("'", "")))

    plt.figure(figsize=(15, 15))
    plt.imshow(wcloud)
    plt.axis('off')
    plt.title('')
    plt.show()
    return render_template('index.html')

 # Search Maximum Donors
@app.route('/donors', methods=['GET', 'POST'])
def donors():
    category = request.form['category']
    cur = mysql.connection.cursor()

    # Get top 30 donors for selected category
    query_sum = "SELECT DonorId,DonationSum,DonationCount from DonorStats where ProjectResourceCategory = %s ORDER BY sum DESC limit 30"
    cur.execute(query_sum, [category, ])
    data = cur.fetchall()

    # Store top 30 donors in dataframe
    col_names = ['DonorId', 'Sum', 'Cost']
    donor_list = pd.DataFrame(list(data))
    donor_list.columns = col_names

    # List of top 30 donors
    donorId = list(donor_list['DonorId'].values)

    # List location of top 30 donors on basis of DonorId
    query_location = "SELECT City,State,Zip,DonorId FROM Donor WHERE DonorId in ({}) limit 30".format(
        ",".join([str(i) for i in donorId]))
    cur.execute(query_location)
    data = cur.fetchall()

    # Store location details for top 30 donors in dataframe
    col_names = ['City', 'State', 'Zip', 'DonorId']
    donor_location = pd.DataFrame(list(data))
    donor_location.columns = col_names

    # merge both dataframes to create view for top 30 donors for each category
    merged_donorlist = pd.merge(
        donor_list, donor_location, left_on='DonorId', right_on='DonorId', how='left')
    print(list(merged_donorlist.values))
    cur.close()
    return render_template('maxdonors.html', maxdonor=list(merged_donorlist.values))

# Search Maximum Utilized Resource Category
@app.route('/resource', methods=['GET', 'POST'])
def resource():
    category = request.form['category']
    cur = mysql.connection.cursor()

    # List max donation for each category
    query = "select ProjectResourceCategory,avg(DonationStrength) from ProjectStats where ProjectResourceCategory = %s"
    cur.execute(query, [category, ])
    data = cur.fetchall()
    cur.close()
    return render_template('maxdonationlist.html', maxdonation=data)

# insert data into database
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == "POST":
    ProjectId=randint(0,1000000)
        teachername = request.form['tname']
        projectname = request.form['pname']
        essay = request.form['essay']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO project(ProjectId,TeacherId,ProjectEssay) VALUES (%s,%s, %s)",
                    (teachername, projectname, essay))
        mysql.connection.commit()
    return render_template('index.html')    

if __name__ == '__main__':
    app.run(debug=True)
