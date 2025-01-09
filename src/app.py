from flask import Flask, render_template
import json
import os

app = Flask(__name__)
_script_dir = os.path.dirname(os.path.abspath(__file__))
PROXY_FILE = os.path.join(os.path.dirname(_script_dir), 'proxies.json')


def load_proxies():
    if not os.path.exists(PROXY_FILE):
        return {}
    try:
        with open(PROXY_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return {}


@app.route('/')
def index():
    proxies = load_proxies()
    return render_template('index.html', proxies=proxies)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
