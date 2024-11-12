# crawler.py
import requests
from bs4 import BeautifulSoup
import concurrent.futures

from database import *
from extractor import *
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def crawl_website(base_url):
    crawl = {base_url}
    conn = init_db()
    count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        while crawl:
            # if depth > max_depth:
            #     break
            row_count = get_row_count(conn)
            if row_count >= 800:
                logging.info(
                    f"Reached the maximum limit of {row_count} rows in the database. Stopping crawl.")
                break
            url = crawl.pop()
            if is_visited(conn, url) or is_crawled(conn, url):
                pass
            # logging.info(f'Crawling URL: {url} at depth {depth}')
            logging.info(f'Crawling URL: {url}')
            mark_visited(conn, url)
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, "html.parser")
                company_name = extract_company_name(soup)
                if not company_name:
                    company_name = extract_title(soup)
                social_links = extract_social_links(url)
                content = get_p_tag_content(soup)
                category = categorize_page_content(content)
                for link in social_links:
                    save_to_db(conn, link, company_name, url, category)
                new_links = get_all_links(url)
                for link in new_links:
                    # crawl.append((link, depth + 1))
                    save_crawled_url(conn, link, url)

                crawl.update(new_links)
                mark_crawled(conn, url)
                count += 1
                if count % 10 == 0:
                    logging.info(f'Processed {count} pages.')
            except requests.RequestException as e:
                logging.error(f"Failed to process {url}: {e}")

    conn.close()


if __name__ == '__main__':
    crawl_website("https://golrang.com")
    print(20 * '*')
    print("Web Scraping Done Successfully!")
    print(20 * '*')
