import sys
import requests
import mysql.connector
import re
import trafilatura
from logger import logger
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from database import (
    get_connection,
    get_or_create_sitemap,
    url_exists,
    get_page_id,
    get_pending_pages,
    update_page_content,
    save_urls,normalize_url
)

from config import (
    DB_CONFIG,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    BATCH_SIZE,
    HEADERS,
    REMOVE_TAGS,
    SKIP_EXTENSIONS
)

logger.basicConfig(level=logger.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

session = requests.Session()
session.headers.update(HEADERS)

def get_sitemap_url(base_url):
    robots_url = urljoin(base_url, "/robots.txt")

    try:
        response = make_request(robots_url)

        for line in response.text.splitlines():
            if line.lower().startswith("sitemap:"):
                return line.split(":", 1)[1].strip()

    except Exception:
        pass

    return urljoin(base_url, "/sitemap.xml")

def make_request(url):

    logger.info(f"Fetching {url}")
    for attempt in range(MAX_RETRIES):

        try:

            response = session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response

        except Exception as e:

            if attempt == MAX_RETRIES - 1:
                raise e

            logger.warning(f"Retry {attempt + 1} for {url}")

def extract_urls_from_sitemap(sitemap_url):

    discovered_urls = []

    try:

        response = make_request(sitemap_url)

        soup = BeautifulSoup(response.content,"xml")

        if soup.find("sitemapindex"):
            child_sitemaps = [loc.text.strip() for loc in soup.find_all("loc")]
            logger.info(f"Found {len(child_sitemaps)} child sitemaps")

            for child_sitemap in child_sitemaps:
                child_urls = extract_urls_from_sitemap(child_sitemap)
                discovered_urls.extend(child_urls)

            return discovered_urls

        urls = [normalize_url(loc.text) for loc in soup.find_all("loc")]

        return urls

    except Exception as e:

        logger.error( f"Failed sitemap: {sitemap_url}")

        logger.error(str(e))

        return []

def clean_markdown(markdown):

    if not markdown:
        return ""

    markdown = re.sub(r'\n{3,}', '\n\n', markdown)

    return markdown.strip()

def html_to_markdown(html):

    try:

        content = trafilatura.extract(
            html,
            output_format="markdown",
            include_links=False,
            include_images=False,
            include_tables=True,
            favor_precision=True,
            deduplicate=True
        )
        

        if not content:
            return ""

        content = clean_markdown(content)

        return content

    except Exception as e:

        logger.error(f"Trafilatura extraction failed: {e}")
        return ""

def process_pages(cursor, conn, sitemap_id):
    rows = get_pending_pages(cursor,sitemap_id)
    total = len(rows)
    logger.info( f"{total} pending pages found")
    success = 0
    failed = 0

    for index, (page_id, url) in enumerate(rows, start=1):
        try:
            logger.info(f"[{index}/{total}] {url}")
            response = make_request(url)
            markdown = html_to_markdown(response.text)
            update_page_content( cursor , conn , page_id , markdown)

            success += 1

            if success % BATCH_SIZE == 0:
                print(f"Committing batch at {success}")
                conn.commit()

        except Exception as e:
            failed += 1
            logger.error(f"Failed URL: {url}")
            logger.error(str(e))

    conn.commit()

    logger.info(f"Completed | Success={success} | Failed={failed}")

def process_website(website):
    conn, cursor = get_connection()
    sitemap_url = get_sitemap_url(website)
    logger.info(f"Website : {website}")
    logger.info(f"Sitemap : {sitemap_url}")

    try:
        urls = extract_urls_from_sitemap(sitemap_url)
        logger.info(f"{len(urls)} URLs discovered")
        if not urls:
            logger.warning("No URLs found in sitemap.")
            return {
                "status": "Failed",
                "website": website,
                "message": "No URLs found. Sitemap deleted."
            }
        sitemap_id = get_or_create_sitemap(cursor, conn, sitemap_url)
        save_urls(cursor, conn, sitemap_id, urls)
        process_pages(cursor, conn, sitemap_id)
        return {
            "status": "Success",
            "website": website,
            "total_urls": len(urls)
        }

    finally:
        cursor.close()
        conn.close()
        logger.info("Database connection closed")

def main():

    if len(sys.argv) > 1:
        website = sys.argv[1].strip()
    else:
        website = input("Enter the website's URL: " ).strip()

    process_website(website)
    
if __name__ == "__main__":
    main()