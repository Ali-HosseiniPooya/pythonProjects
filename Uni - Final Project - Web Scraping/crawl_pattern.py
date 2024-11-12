# crawl_pattern.py
from flask import Flask, jsonify, render_template
from database import *
app = Flask(__name__)


def get_relationship_data():
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT url, parent_url FROM crawled_urls")
    data = c.fetchall()
    conn.close()
    return data


@app.route('/api/crawled-data')
def crawled_data():
    data = get_relationship_data()
    # Flatten and deduplicate
    nodes = list(set([item for sublist in data for item in sublist]))
    nodes = [{'id': node} for node in nodes]
    links = [{'source': parent, 'target': child} for parent, child in data]
    return jsonify({'nodes': nodes, 'links': links})


@app.route('/')
def index():
    return render_template('crawl_pattern.html')


if __name__ == '__main__':
    app.run(debug=True)
