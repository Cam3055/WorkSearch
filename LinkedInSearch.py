from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import argparse

# Path to your ChromeDriver executable
chrome_driver_path = '"C:\\Users\\caman\\OneDrive\\Desktop\\Scalper\\chromedriver.exe"\\chromedriver.exe"'
username = ""
password = ""
# Path to your Chrome browser executable



def linkQuickSearch(company_name, employee_name):
    # Specify the path to the ChromeDriver executable
        # Initialize ChromeDriver with custom options
    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")  # Maximize the browser window
    options.add_argument("--disable-infobars")  # Disable the "Chrome is being controlled by automated software" message

    # Specify the path to the ChromeDriver executable
    service = Service(chrome_driver_path)

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the LinkedIn login page
    driver.get('https://www.linkedin.com/login')

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
        print('Login successful!')
    else:
        print('Login failed.')
        driver.quit()
        exit()

    # Search for the company
    search_box = driver.find_element(By.XPATH, '//input[contains(@placeholder, "Search")]')
    search_box.send_keys(employee_name)
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
        print(f"{employee_name} works at {company_name}.")
    else:
        print(f"{employee_name} does not work at {company_name}.")

    # Close the browser
    driver.quit()
#Test







def linkSearchLong(company_name, employee_name):
    # LinkedIn credentials


    # Initialize ChromeDriver with custom options
    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")  # Maximize the browser window
    options.add_argument("--disable-infobars")  # Disable the "Chrome is being controlled by automated software" message

    # Specify the path to the ChromeDriver executable
    service = Service(chrome_driver_path)

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the LinkedIn login page
    driver.get('https://www.linkedin.com/login')

    # Find the email and password input fields and enter the credentials
    email_field = driver.find_element(By.ID, 'username')
    email_field.send_keys(username)

    password_field = driver.find_element(By.ID, 'password')
    password_field.send_keys(password)

    # Submit the form
    password_field.submit()

    # Wait for the login process to complete


    # Verify if login was successful
    import time
    time.sleep(4)
    if driver.current_url == 'https://www.linkedin.com/feed/':
        print('Login successful!')
    else:
        print('Login failed.')
        driver.quit()
        exit()

    # Search for the company
    search_box = driver.find_element(By.XPATH, '//input[contains(@placeholder, "Search")]')
    search_box.send_keys(company_name)
    search_box.send_keys(Keys.RETURN)


    print(driver.current_url)
    # Click on the "People" tab to filter the search results

    driver.implicitly_wait(4)

    # people_tab = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div[1]/div/div/div/section/ul/li[3]/button')
    # people_tab.click()


    people_tab = driver.find_element(By.LINK_TEXT, 'See all people results')
    people_tab.click()

    # peopleResults= driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/div[2]')
    # peopleResults.click()


    while True:
        try:
            # Check if the employee exists in the current page
            
            try:    
                employee_element = driver.find_element(By.XPATH, f'//span[contains(text(), "{employee_name}")]')
                return(f"{employee_name} works at {company_name}.")
            except:

                name_parts = employee_name.split()
                name = name_parts[0]
                surname = name_parts[-1]
                # Get the first letter of the surname
                first_letter_surname = surname[0]+"."
                # Format the name as "Name, First Letter of Surname"
                formatted_name = f"{name}, {first_letter_surname}"
                employee_element = driver.find_element(By.XPATH, f'//span[contains(text(), "{formatted_name}")]')
                return(f"{employee_name} works at {company_name}.")

        except NoSuchElementException:
            # Continue to the next page if available
            try:
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    next_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[5]/div/div/button[2]')
                    next_button.click()
                except:
                    next_button = driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[2]/div/div[2]/div/button[2]')
                    next_button.click()
                
                
            except NoSuchElementException:
                
                # No more pages available, employee not found
                print(f"{employee_name} does not work at {company_name}.")
                


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description='JobSearch.')
    
    # Add arguments with desired variable names and types
    parser.add_argument('--employee_name', type=str, default='Jason Thompson', help='Name of employee.')
    parser.add_argument('--company_name', type=str, default='JETMS', help='Name of company.')
    # parser.add_argument('--flag', action='store_true', help='Flag argument.')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the variables using the argument names defined above
    employee_name = args.employee_name
    company_name = args.company_name

    print(linkQuickSearch(company_name,employee_name))
   

if __name__ == '__main__':
    main()
