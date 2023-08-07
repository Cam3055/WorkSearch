from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import argparse


# Path to your Chrome browser executable
def linkDriverinit():
    chrome_driver_path = "chromedriver.exe"
    

    # Specify the path to the ChromeDriver executable
        # Initialize ChromeDriver with custom options
    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")  # Maximize the browser window
    options.add_argument("--disable-infobars")  # Disable the "Chrome is being controlled by automated software" message

    # Specify the path to the ChromeDriver executable
    service = Service(chrome_driver_path)

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.linkedin.com/login')
    return(driver)


def linkLoginInit(driver):


    username = "cam.anderson123@gmail.com"
    password = "Secretspy123"
    # Find the email and password input fields and enter the credentials
    email_field = driver.find_element(By.ID, 'username')
    email_field.send_keys(username)

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(password)
    
    # Submit the form
    password_field.submit()

    # Wait for the login process to complete
    driver.implicitly_wait(10)

    # Verify if login was successful
    if driver.current_url == 'https://www.linkedin.com/feed/':
        return True
    else:
        return False

def linkSearch(driver,company_name,employee_name):
    # Search for the company
    search_box = driver.find_element(By.XPATH, '//input[contains(@placeholder, "Search")]')
    search_box.send_keys(employee_name," ",company_name)
    search_box.send_keys(Keys.RETURN)

    # Check if the person works for the specified company
    person_works_at_company = False
    try:
        # Look for the person's profile in the search results
        person_profile = driver.find_element(By.XPATH, f'//span[contains(text(), "{employee_name}")]')

        # Click on the person's profile to check their employment information
        person_profile.click()

        # Check if the company name is mentioned on the person's profile
        employment_info = driver.find_element(By.XPATH, f'//span[contains(text(), "{company_name}")]')
        person_works_at_company = True
    except:
        pass

    # Print the result
    if person_works_at_company:
        return driver, True
    else:
        return driver, False
#Test




                


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='JobSearch.')
    
    # Add arguments with desired variable names and types
    parser.add_argument('--employee_name', type=str, default='James Date', help='Name of employee.')
    parser.add_argument('--company_name', type=str, default='Babcock', help='Name of company.')
    # parser.add_argument('--flag', action='store_true', help='Flag argument.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the variables using the argument names defined above
    employee_name = args.employee_name
    company_name = args.company_name

    print(linkQuickSearch(company_name,employee_name))
   

if __name__ == '__main__':
    main()
