from flask import Flask, request, send_file
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <form action="/scrape" method="post">
            <label for="url">Enter URL:</label>
            <input type="text" id="url" name="url">
            <input type="submit" value="Scrape">
        </form>
    '''

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract data (example: all links)
    course_numbers = []
    for course in soup.find_all(text=True):
        if ' - ' in course and course.split(' - ')[0].isupper():
            course_numbers.append(course.split(' - ')[0])

    # Write data to Excel
    workbook = Workbook()
    sheet = workbook.active
    for row, item in enumerate(data, start=1):
        sheet.cell(row=row, column=1, value=item)
    filename = 'output.xlsx'
    workbook.save(filename)

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)