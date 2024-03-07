from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape_metadata(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.string if soup.title else "No title found"

    meta_description = ''
    meta_tag = soup.find('meta', attrs={'name': 'description'})

    if meta_tag:
        meta_description = meta_tag['content']

    return { 'title': title, 'meta_description': meta_description }


@app.route('/get-link-info', methods=['GET'])
def get_link_info():
    url = request.args.get('url')

    if not url:
        return jsonify({'error': 'URL parameter is missing'}), 400

    try:
        metadata = scrape_metadata(url)
        return jsonify(metadata), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
