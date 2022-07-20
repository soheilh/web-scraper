from tabulate import tabulate
import requests, time
import pandas as pd
from bs4 import BeautifulSoup

# Place your URL here
URL = "https://khatam.ac.ir/page/4582319/%D8%A2%D8%B2%D9%85%D9%88%D9%86%E2%80%8C%D9%87%D8%A7%DB%8C%20%D8%A8%DB%8C%D9%86%E2%80%8C%D8%A7%D9%84%D9%85%D9%84%D9%84%DB%8C/TOEFL/%D8%AA%D8%A7%D8%B1%DB%8C%D8%AE%20%D8%A2%D8%B2%D9%85%D9%88%D9%86"

# Put your status here to compare with the data in the URL
status_list = ['ACTIVE', 'ACTIVE', 'ACTIVE', 'ACTIVE', 'ACTIVE', 'INACTIVE', 'INACTIVE', 'ACTIVE', 'INACTIVE', 'INACTIVE', 'INACTIVE', 'ACTIVE', 'INACTIVE', 'ACTIVE', 'ACTIVE', 'INACTIVE', 'INACTIVE', 'ACTIVE', 'INACTIVE', 'ACTIVE', 'INACTIVE', 'INACTIVE', 'ACTIVE', 'INACTIVE', 'INACTIVE', 'INACTIVE', 'ACTIVE', 'INACTIVE']


# For Colors text in terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function for get data from URL and return as DataFrame
def get_table(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    rows = []
    for child in soup.find('table'):
        for tr in child:
            row = []
            try:
                for td in tr:
                    row.append(td.text)
            except:
                continue
            rows.append(row)

    df = pd.DataFrame(rows[1:], columns=['index', 'day', 'date(shamsi)', 'date', 'status'])
    return df

# Function to detect status changes
def recognize_status(data, status):
    status_list = data['status'].tolist()
    list_of_changes = []
    for index in range(len(status_list)):
        if status_list[index] != status[index]:
            list_of_changes.append(index)
    return list_of_changes


# Main While Loop
while 1:
    data = get_table(URL)
    list_of_changes = recognize_status(data, status_list)
    if list_of_changes:
        print(bcolors.OKGREEN + 'Something was found:' + bcolors.ENDC)
        print(tabulate(data.loc[list_of_changes], headers='keys', tablefmt='pretty'))

    else:
        print(bcolors.OKGREEN + "Nothing Found :(" + bcolors.ENDC)

    time.sleep(5)
