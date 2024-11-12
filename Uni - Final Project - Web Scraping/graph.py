# graph.py
from flask import Flask, render_template, jsonify
from database import *

app = Flask(__name__)

# Category colors
category_colors = {
    'مواد اولیه': "red",
    'صنایع': "blue",
    "کالاهای مصرفی": "purple",
    "دارو و سلامت": "orange",
    "خدمات مالی": "pink",
    "خدمات مصرف کننده": "cyan",
    "تکنولوژی": "yellow"
}


def get_relationship_data():
    """Fetch data from the database."""
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT category, company_name FROM social_links")
    rows = c.fetchall()
    conn.close()
    return rows


@app.route('/api/graph-data')
def graph_data():
    """Get graph data and convert to JSON."""
    data = get_relationship_data()

    # Extract unique categories and companies
    categories = set()
    companies = set()

    for category, company in data:
        categories.add(category)
        if company:
            companies.add(company)

    # Prepare nodes with colors
    nodes = [{'id': cat, 'color': category_colors.get(
        cat, 'gray')} for cat in categories]
    nodes += [{'id': comp, 'color': 'green'}
              for comp in companies]  # Default company color

    # Prepare links
    links = [{'source': category, 'target': company}
             for category, company in data if company]

    return jsonify({'nodes': nodes, 'links': links})


@app.route('/')
def index():
    return render_template('graph.html')


if __name__ == "__main__":
    app.run(debug=True)
