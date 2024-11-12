# extractor.py
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Dict
import logging


def extract_company_name(soup: BeautifulSoup) -> str:
    potential_classes = [
        'img-responsive img-companies', 'title-brands',
        # Add other potential classes here if they differ across categories
    ]

    for class_name in potential_classes:
        img_tag = soup.find('img', class_=class_name)
        h1_tag = soup.find('h1', class_=class_name)
        if h1_tag:
            # Extract the h1 tag
            title = h1_tag.get('title-brands')
            return title
        elif img_tag:
            # Extract the title or alt attribute
            title = img_tag.get('title')
            alt = img_tag.get('alt')
            logging.info(f"Found company name: {title or alt}")
            return title or alt  # Return title if available, otherwise alt
    logging.warning("No company name found")
    return None


def extract_title(soup: BeautifulSoup) -> str:
    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.get_text(strip=True)
        logging.info(f"Using title tag for company name: {title}")
        return title
    logging.warning("No title tag found")
    return None


def extract_website_title(url: str) -> str:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        return extract_title(soup)
    except requests.RequestException:
        logging.error(f"Failed to retrieve title from {url}")
        return None


def get_all_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        base_netloc = urlparse(url).netloc
        exclude_pattern = re.compile(
            r'event|printable|ajax-brand-red|ajax-company-red|news', re.IGNORECASE)
        include_pattern = re.compile(
            r'brands|company|companies|brand', re.IGNORECASE)
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            link_netloc = urlparse(full_url).netloc

            if link_netloc == base_netloc:
                # Exclude URLs that match the exclude pattern
                if not exclude_pattern.search(full_url):
                    links.append(full_url)
                    # Include URLs that match the include pattern
                    if include_pattern.search(full_url):
                        links.append(full_url)
                    else:
                        pass

        logging.info(f"Found {len(links)} links on {url}")
        return links

    except requests.RequestException as e:
        logging.error(f"Failed to retrieve links from {url}: {e}")
        return set()


# Function to extract social media links from a page
def extract_social_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        social_links = []

        social_media_pattern = re.compile(
            r"https://(?:t\.me|www\.instagram\.com|www\.twitter\.com|www\.facebook\.com|www\.whatsapp\.com|www\.x\.com|www\.linkedin\.com)/[^\s]+",
            re.IGNORECASE)

        for link in soup.find_all('a', href=True):
            href = link["href"]
            if social_media_pattern.search(href):
                social_links.append(href)
        return social_links
    except requests.RequestException:
        logging.error(f"Failed to extract social links from {url}")
        return []


def get_p_tag_content(soup: BeautifulSoup) -> str:
    paragraphs = soup.find_all('p')
    return ' '.join(p.get_text(strip=True) for p in paragraphs)


def get_category_patterns() -> Dict[str, re.Pattern]:
    return {
        "مواد اولیه": re.compile(r'\b(مواد اولیه)\b', re.IGNORECASE),
        "صنایع": re.compile(r'\b(صنعت|کارخانه|صنایع|تولیدی)\b', re.IGNORECASE),
        "کالاهای مصرفی": re.compile(r'\b(شوینده|آرایشی|غذایی|مایع|نرم کننده|سفید کننده|پاک کننده|محصولات مصرفی)\b', re.IGNORECASE),
        "دارو و سلامت": re.compile(r'\b(دارو|دارویی|سلامت|بهداشتی|پزشکی|بهداشت)\b', re.IGNORECASE),
        "خدمات مالی": re.compile(r'\b(سرمایه‌گذار|سرمایه‌گذاری|نهاد مالی|مالی|ارزش آفرین|لیزینگ|بانکی|بیمه)\b', re.IGNORECASE),
        "خدمات مصرف کننده": re.compile(r'\b(تجهیزات|سینما|فرهنگی|مال|هایپرمارکت|فروشگاه‌های زنجیره‌ای|فروشگاه زنجیره‌ای|خدمات مصرفی)\b', re.IGNORECASE),
        "تکنولوژی": re.compile(r'\b(اپلیکیشن|IT|دیجیتال|رایانه‌ای|کامپیوتری|سخت‌افزاری|فناوری|تکنولوژی)\b', re.IGNORECASE)
    }


def match_category(content: str, pattern: re.Pattern) -> bool:
    return bool(pattern.search(content))


def categorize_page_content(content: str) -> str:
    if not content:
        return "دسته بندی نشده"

    category_patterns = get_category_patterns()

    for category, pattern in category_patterns.items():
        if match_category(content, pattern):
            return category

    return "دسته بندی نشده"
