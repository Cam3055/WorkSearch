import zenoh
import json
import numpy as np
import WebSearch
import time


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


# Function to process the NumPy array
def process_data(data):
    # Example processing: square all elements
    result = np.square(data)
    return result

import ast
def listener(sample,driver):
    # Check if there is new data
    if sample is not None:
        print('Data Recieved')
        # Parse the JSON data from Zenoh
        list_to_search = sample.payload.decode('utf-8')
        # Convert the JSON data to a NumPy array
        # numpy_array = np.array(json_data)
        list_to_search = ast.literal_eval(list_to_search)
        # Process the NumPy array
        searchList=""
        for i in list_to_search:
            driver,sdata=linkSearchEmployee(driver,i[0],i[1])
            # searchList = (searchList+str(sdata[0])+','+str(sdata[1])+','+str(sdata[2])+','+str(sdata[3])+"\n")
            data = [{'company_name': sdata[0],'employee_name': sdata[1],'record': sdata[2],'url': sdata[3]}]
            session = zenoh.open()
            key = "vm1/answer"
            pub = session.declare_publisher(key)
            pub.put(data)
        # Print or use the processed data as needed
        print("Processed data")

    print(f"Received {sample.kind} ('{sample.key_expr}': '{sample.payload.decode('utf-8')}')")


def main():  
    session = zenoh.open()
    # Define the Zenoh query for your data
    key = "vm1/search"
    # Create a Zenoh workspace
    driver = linkStartUp()
    sub = session.declare_subscriber(key,lambda sample:listener(sample,driver))
    while True:
        pass
    
    
if __name__ == "__main__":
    main()
