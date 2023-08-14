from flask import Flask, render_template, request, redirect, url_for, jsonify

import WebSearch
import numpy as np
import time
import csv
import io
import os
app = Flask(__name__)


@app.route('/')



def index():
    return render_template('index.html')


    

# Get the uploaded files
@app.route("/", methods=['POST'])
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
        searchList = linkSearchList(driver,searchList)
    return jsonify({'result': (searchList[0][2],searchList[1][2],searchList[2][2])})

def linkStartUp():
    driver = WebSearch.linkDriverinit()
    WebSearch.linkLoginInit(driver=driver)
    return driver

def linkSearchList(driver,searchList):
    searchResult = []
    for i in searchList:
        driver,result =WebSearch.linkSearch(driver,i[0], i[1])
        time.sleep(3)
        if result == True:
            searchResult.append([i[0],i[1],"Record Found"])
        else:
            searchResult.append([i[0],i[1],"No Record Found"])
    return searchResult
            
    #         return f'<h1>CSV file processed!</h1><p>{searchList[0:]}</p>'
    # return render_template('index.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)