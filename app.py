from flask import Flask, render_template, request, Response, redirect, url_for, session, flash, jsonify
import mysql.connector
from waitress import serve
import WebSearch
import numpy as np
import time
import csv
import io
from flask_socketio import SocketIO, emit
import os
app = Flask(__name__)
socketio = SocketIO(app)



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



# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         connection = get_db_connection()
#         if connection:
#             cursor = connection.cursor(dictionary=True)
#             try:
#                 cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
#                 connection.commit()
#                 cursor.close()
#                 connection.close()
#                 flash("Account created successfully!", "success")
#                 return redirect(url_for('login'))
#             except mysql.connector.Error as err:
#                 flash(f"Error: {err}", "danger")
#                 return redirect(url_for('signup'))

#     return render_template('signup.html')



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


@app.route("/results", methods=['GET'])
def resultPage():
    return render_template('results.html')

@socketio.on('message', namespace='/update_table')





@app.route("/resultSearch", methods=['POST'])
def populate():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_content = uploaded_file.read().decode('utf-8')
        csv_reader = csv.reader(io.StringIO(file_content))
        searchList = [row for row in csv_reader]
        searchList = searchList[1:]
        driver = linkStartUp()
        # time.sleep(20)
        for i in searchList:
            driver,data= linkSearchEmployee(driver,i[0],i[1])
            socketio.send('update_table', {
            'company_name': data[0],
            'employee_name': data[1],
            'record': data[2],
            'url': data[3]})
    return render_template('results.html')
        



if __name__ == '__main__':
#     serve(app,host='0.0.0.0',port=80)
    socketio.run(app,host='127.0.0.1',port=80,debug=True)