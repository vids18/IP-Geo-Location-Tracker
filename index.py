from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_pymongo import pymongo
import datetime
from pymongo import MongoClient
from ip2geotools.databases.noncommercial import DbIpCity
from datetime import datetime
import pymongo
import json



app = Flask(__name__)

##################################################
cluster= MongoClient("mongodb+srv://vidhi:1234@cluster0-dqsmj.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]
##############################################
@app.route("/")
def getreg():
    return render_template('getreg.html')
#####################################################
@app.route("/get_reg",methods=['POST', 'GET'])
def get_reg():    
##################################################################
    
    if request.method == 'POST': #this block is only entered when the form is submitted
        user= request.form['ipaddress']
        response = DbIpCity.get(user, api_key='free')
        print(response.city)
        cluster= MongoClient("mongodb+srv://vidhi:1234@cluster0-dqsmj.mongodb.net/test?retryWrites=true&w=majority")
        db = cluster["test"]
        collection = db["test"]
        
        post = {"IP_Address": user, "City": response.city, 'time': datetime.datetime.now()}
        collection.insert_one(post)
        return 'submitted'
    return render_template('getreg.html')
#################################################################

@app.route("/lochist", methods=["GET","POST"])
def lochist():
    if request.method =="POST":
        myclient = pymongo.MongoClient("mongodb+srv://vidhi:1234@cluster0-dqsmj.mongodb.net/test?retryWrites=true&w=majority")
        mydb = myclient["test"]
        mycol = mydb["test"]
        x = mycol.find_one()
        number= request.form['number']
        cursor = mycol.find({})
        temp = []
        
        i=0
        for document in cursor:
            
            if i<int(number):
                temp.append(document)
            i=i+1
        #print(number)
        return render_template('lochist.html', document=temp)
    return render_template('getreg.html')
##################################################################
@app.route("/date_time", methods=["GET","POST"])
def date_time():
    if request.method=="POST":
        myclient = pymongo.MongoClient("mongodb+srv://vidhi:1234@cluster0-dqsmj.mongodb.net/test?retryWrites=true&w=majority")
        mydb = myclient["test"]
        mycol = mydb["test"]
        
        from_year = request.form['fromyear']
        from_year=int(from_year)
        
        to_year = request.form['toyear']
        to_year=int(to_year)
        
        from_month = request.form['frommonth']
        from_month= int(from_month)
        
        to_month = request.form['tomonth']
        to_month= int(to_month)
        
        from_day = request.form['fromday']
        from_day= int(from_day)
        
        to_day = request.form['today']
        to_day= int(to_day)
        
        from_hour = request.form['fromhour']
        from_hour= int(from_hour)
        
        to_hour = request.form['tohour']
        to_hour = int(to_hour)
        
        from_mins = request.form['frommins']
        from_mins= int(from_mins)
        
        to_mins = request.form['tomins']
        to_mins= int(to_mins)
        
        from_secs = request.form['fromsecs']
        from_secs= int(from_secs)
        
        to_secs = request.form['tosecs']
        to_secs= int(to_secs)
        start= datetime(from_year,from_month, from_day,from_hour,from_mins,from_secs)
        end = datetime(to_year,to_month, to_day, to_hour, to_mins,to_secs )
        p= mycol.find_one({'time':{'$lte':end,'$gte':start}})
        print(p)
        temp = []
        i=0
        for document1 in p:
            if i<len(p):
                temp.append(document1)
            i=i+1
        return render_template('date_time.html', document1=temp)
    return render_template('getreg.html')
######################################################
if __name__ == "__main__":
    app.run()
