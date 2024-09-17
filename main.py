import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# Function to fetch and parse webpage
def fetch_webpage(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

# Function to extract data (example: extracting all links)
def extract_data(soup):
    data = []
    for link in soup.find_all('a'):
        data.append(link.get('href'))
    return data

# Function to write data to Excel
def write_to_excel(data, filename):
    workbook = Workbook()
    sheet = workbook.active
    for row, item in enumerate(data, start=1):
        sheet.cell(row=row, column=1, value=item)
    workbook.save(filename)

# Main script
url = 'https://catalog.colostate.edu/general-catalog/colleges/natural-sciences/physics/physics-minor/#requirementstext'
soup = fetch_webpage(url)
if soup:
    data = extract_data(soup)
    write_to_excel(data, 'output.xlsx')
