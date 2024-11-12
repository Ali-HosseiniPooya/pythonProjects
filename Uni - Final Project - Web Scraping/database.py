# database.py
import sqlite3


def init_db():
    conn = sqlite3.connect("social_links.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS social_links
                 (id INTEGER PRIMARY KEY, social_link TEXT UNIQUE, company_name TEXT, website_link TEXT, category TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS visited_urls
                 (url TEXT PRIMARY KEY)''')
    c.execute('''CREATE TABLE IF NOT EXISTS crawled_urls 
                 (url TEXT PRIMARY KEY, parent_url TEXT)''')
    conn.commit()
    return conn


def save_to_db(conn, social_link, company_name, website_link, category):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO social_links (social_link, company_name, website_link, category) VALUES (?, ?, ?, ?)",
                  (social_link, company_name, website_link, category))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore duplicates


def mark_visited(conn, url):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO visited_urls (url) VALUES (?)", (url,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore duplicates


def mark_crawled(conn, url):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO crawled_urls (url) VALUES (?)", (url,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore duplicates


def save_crawled_url(conn, url, parent_url):
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO crawled_urls (url, parent_url) VALUES (?, ?)", (url, parent_url))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Ignore duplicates


def is_visited(conn, url):
    c = conn.cursor()
    c.execute("SELECT 1 FROM visited_urls WHERE url=?", (url,))
    return c.fetchone() is not None


def is_crawled(conn, url):
    c = conn.cursor()
    c.execute("SELECT 1 FROM crawled_urls WHERE url=?", (url,))
    return c.fetchone() is not None


def get_row_count(conn):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM crawled_urls')
    return c.fetchone()[0]
