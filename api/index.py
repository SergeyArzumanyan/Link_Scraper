from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)

def scrape_metadata(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title.string if soup.title else "No title found"

    description = ''
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    if meta_tag:
        description = meta_tag['content']

    favicon = ''
    favicon_link = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
    if favicon_link and favicon_link.has_attr('href'):
        favicon = urljoin(url, favicon_link['href'])

    return {
        'title': title,
        'description': description,
        'image': favicon
    }

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
    print("Running the Flask application...")
    app.run(debug=True)
else:
    print("This script is being imported, not run directly.")