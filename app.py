from flask import Flask, render_template, request, Response
from waitress import serve
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
            
    #         return f'<h1>CSV file processed!</h1><p>{searchList[0:]}</p>'
    # return render_template('index.html')
@app.route("/download", methods=['GET'])
def download():
    return Response("[cam,cam,not]\n[cam,not,cam]\n[not,cam,cam]",
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=download.csv"})


if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)
    # app.run(port=5000,debug=True)