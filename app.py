from flask import Flask, render_template, request, Response, redirect, url_for, session, flash, jsonify
import mysql.connector
import WebSearch
import numpy as np
import time
import csv
import io
from flask_socketio import SocketIO
import os
app = Flask(__name__)
socketio = SocketIO(app)


class listManager:
    def __init__(self):
        self.data_list = []
        self.submitted = False

    

list_manager = listManager()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def searchPage():
    return render_template('search.html')


# Get the uploaded files
@app.route("/linksearch", methods=['POST'])
def uploadFiles():
      # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_content = uploaded_file.read().decode('utf-8')
        csv_reader = csv.reader(io.StringIO(file_content))
        searchList = [row for row in csv_reader]
        searchList = searchList[1:]
        driver = linkStartUp()
        # time.sleep(20)
        responce = "Company,Employee,Status,Url\n"
        searchList = linkSearchList(driver,searchList)
        for i in range(len(searchList)):
            for x in searchList[i]:
                responce=responce+x+","
            responce=responce+"\n"
    return Response(responce,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=employeecheck.csv"})

def linkStartUp():
    driver = WebSearch.linkDriverinit()
    WebSearch.linkLoginInit(driver=driver)
    return driver

def linkSearchList(driver,searchList):
    searchResult = []
    for i in searchList:
        driver,result,url =WebSearch.linkSearch(driver,i[0], i[1])
        time.sleep(3)
        if result == True:
            searchResult.append([i[0],i[1],"Record Found",url])
        else:
            searchResult.append([i[0],i[1],"No Record Found"])
    return searchResult

def linkSearchEmployee(driver,companyName,employeeName):
    
    driver,result,url =WebSearch.linkSearch(driver,companyName,employeeName)
    time.sleep(3)
    if result == True:
        searchResult =[companyName,employeeName,"Record Found",url]
    else:
        searchResult =[companyName,employeeName,"No Record Found","n/a"]
    return driver,searchResult
            


# app = Flask(__name__)
# app.secret_key = "your_secret_key_here"  # Needed for session to work, choose a secure key.

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='camserver',
            user='lhost',
            password='McDevface123!!',
            database='recruitmenteye'
        )   
        return connection
    except mysql.connector.Error as error:
        print(f"Error connecting to database: {error}")
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            if user:
                session['loggedin'] = True
                session['email'] = user['email']
                session['user_id'] = user['id']
                
                return redirect(url_for('dashboard'))
            else:
                return "Incorrect username/password!"

    return render_template('dashboard.html')


@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        return f"Hello, {session['username']}! Welcome to the dashboard."
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route("/upload", methods=['GET'])
def resultPage():
    return render_template('upload.html')


@app.route("/nicktest", methods=['GET'])
def nickpage():
    return render_template('upload.html')

# @socketio.on('message', namespace='/update_table')


@app.route("/result", methods=['POST'])
def populate():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_content = uploaded_file.read().decode('utf-8')
        csv_reader = csv.reader(io.StringIO(file_content))
        searchList = [row for row in csv_reader]
        searchList = searchList[1:]
        list_manager.data_list=searchList
        list_manager.submitted=True
    return render_template('results.html')
        

@socketio.on('request-data')
def test_connect():
    if list_manager.submitted:
        list_manager.submitted = False
        searchList =""
        driver = linkStartUp()
        for i in list_manager.data_list:
            driver,sdata=linkSearchEmployee(driver,i[0],i[1])
            searchList = (searchList+str(sdata[0])+','+str(sdata[1])+','+str(sdata[2])+','+str(sdata[3])+"\n")
            data = [{'company_name': sdata[0],'employee_name': sdata[1],'record': sdata[2],'url': sdata[3]}]
            socketio.emit('update_table', {'data': data})
            # socketio.sleep(5)
    return Response(searchList,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=employeecheck.csv"})



import zenoh
@socketio.on('zenoh-request-data')
def test_connect():
    if list_manager.submitted:
        list_manager.submitted = False
        session = zenoh.open()
        key = "search/vm1"
        pub = session.declare_publisher(key)
        pub.put(list_manager.data_list)
        # searchList =""
        # for i in list_manager.data_list:
        #     driver,sdata=linkSearchEmployee(driver,i[0],i[1])
        #     searchList = (searchList+str(sdata[0])+','+str(sdata[1])+','+str(sdata[2])+','+str(sdata[3])+"\n")
        #     data = [{'company_name': sdata[0],'employee_name': sdata[1],'record': sdata[2],'url': sdata[3]}]
        #     emit('update_table', {'data': data})
            # socketio.sleep(5)
    # return Response(searchList,
    #     mimetype="text/csv",
    #     headers={"Content-disposition":
    #              "attachment; filename=employeecheck.csv"})


if __name__ == '__main__':
    # serve(app,host='0.0.0.0',port=80)
    socketio.run(app,host='127.0.0.1',port=80,debug=True)