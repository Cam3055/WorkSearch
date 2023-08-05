from flask import Flask, request, jsonify, render_template
import WebSearch
import numpy as np
import time
import csv
import io
app = Flask(__name__)


@app.route('/')

def index():
    return render_template('index.html')

@app.route('/h', methods=['GET','POST'])  # Ensure the route supports POST requests
def calculate():
    data = request.json
    companyname = data.get('string1')
    employeename = data.get('string2')
    driver = WebSearch.linkDriverinit()
    WebSearch.linkLoginInit(driver=driver)
    searchList = ["Watson-Marlow","Dominic Anderson"],["Watson Marlow","Lewis Westcott"]

    for i in searchList:
        driver,result =WebSearch.linkSearch(driver,i[0], i[1])
        time.sleep(10)
        if result == True:
            i.append("Record found: "+i[0]+" employees "+i[1])
        else:
            i.append("No record for "+i[0]+" employing "+i[1])
    return jsonify({'result': (searchList[0][2],searchList[1][2])})

def upload_file():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_content = uploaded_file.read().decode('utf-8')
            csv_reader = csv.reader(io.StringIO(file_content))
            searchList = [row for row in csv_reader]
            for i in searchList:
                driver,result =WebSearch.linkSearch(driver,i[0], i[1])
                time.sleep(10)
                if result == True:
                    i.append("Record found: "+i[0]+" employees "+i[1])
                else:
                    i.append("No record for "+i[0]+" employing "+i[1])
        
            
            return f'<h1>CSV file processed!</h1><p>{searchList[0:]}</p>'
    return render_template('index.html')




if __name__ == '__main__':
    app.run(port=5001)