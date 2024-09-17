from flask import Flask, request, send_file
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import io

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract data based on the provided HTML structure
    classes = []
    for row in soup.select('table.sc_courselist tbody tr'):
        cols = row.find_all('td')
        if len(cols) == 3:
            class_code = cols[0].text.strip()
            class_name = cols[1].text.strip()
            credits = cols[2].text.strip()
            classes.append([class_code, class_name, credits])

    for row in soup.select('table.sc_plangrid tbody tr'):
        cols = row.find_all('td')
        if len(cols) == 3:
            class_code = cols[0].text.strip()
            class_name = cols[1].text.strip()
            credits = cols[2].text.strip()
            classes.append([class_code, class_name, credits])

    # Generate CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Class Code', 'Class Name', 'Credits'])
    writer.writerows(classes)
    output.seek(0)

    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='classes.csv')

if __name__ == '__main__':
    app.run(debug=True)
