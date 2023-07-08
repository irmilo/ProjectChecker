from flask import Flask, jsonify, request, send_file, url_for
from flask_cors import CORS
import requests
import json

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/styles.css')
def serve_css():
    return send_file('styles.css')

@app.route('/api/check', methods=['GET'])
def check_availability():
    projectname = request.args.get('projectname')
    shopid = request.args.get('shopid')

    if projectname:
        urls = [
                f"https://api.starterapp.ru/{projectname}/delivery/types",
                f"https://api.starterapp.ru/{projectname}/payment/types",
                #f"https://api.starterapp.ru/{projectname}/settings",
                f"https://api.starterapp.ru/{projectname}/categories/{shopid}/v2",
                #f"https://api.starterapp.ru/{projectname}/meals/{shopid}/v2",
                f"https://api.starterapp.ru/{projectname}/settings/headerWeb",
                f"https://api.starterapp.ru/{projectname}/settings/headerApp",
                f"https://api.starterapp.ru/{projectname}/pagemeta",
                f"https://api.starterapp.ru/{projectname}/delivery/shops",
                f"https://api.starterapp.ru/{projectname}/references/settings",
                f"https://api.starterapp.ru/{projectname}/references/faq",
                f"https://api.starterapp.ru/{projectname}/references/banners",
                f"https://static.content.starterapp.co/api/{projectname}/info_pages",
                f"https://settings.api.starterapp.co/{projectname}/frontend",
                f"https://settings.api.starterapp.co/{projectname}/frontend/locales",
                #f"https://settings.api.starterapp.co/{projectname}/loyalty",
                #f"https://settings.api.starterapp.co/{projectname}/app",
                #f"https://api.starterapp.ru/{projectname}/meals/update"
        ]

        responses = {}
        for url in urls:
            response = send_get_request(url)
            responses[url] = response

        return jsonify(responses)
    else:
        return jsonify({'error': 'Project name is required'})

def send_get_request(url):
    try:
        response = requests.get(url)
        if response.ok:
            try:
                return response.json()
            except json.JSONDecodeError as e:
                return str(e)
        else:
            return str(response.status_code) + " " + response.reason
    except requests.exceptions.RequestException as e:
        return str(e)

if __name__ == '__main__':
    app.run()
