from logger import get_logger
import mysql.connector
from config import DB_CONFIG ,  SKIP_EXTENSIONS

logger = get_logger("DATABASE")

def get_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    return conn, cursor

def normalize_url(url):
    return url.strip().rstrip("/")

def url_exists(cursor , sitemap_id , url):
    cursor.execute("Select Id from sitemap_pages where Sitemap_ID =%s AND Url =%s " , (sitemap_id,url))
    return cursor.fetchone() is not None

def get_pending_pages(cursor,sitemap_id):
    cursor.execute("SELECT Id, Url FROM sitemap_pages WHERE Sitemap_ID = %s AND Page_Scrapped IS NULL", (sitemap_id,) )
    return cursor.fetchall()

def update_page_content(cursor , conn , page_id, markdown):
    cursor.execute("UPDATE sitemap_pages SET Page_Scrapped = %s WHERE Id = %s", ( markdown , page_id))

def update_page_summary(cursor, conn, page_id, summary):
    cursor.execute("UPDATE sitemap_pages SET Page_Summary = %s WHERE Id = %s", (summary, page_id))
    conn.commit()

def get_or_create_sitemap(cursor, conn, sitemap_url):
    sitemap_url = normalize_url(sitemap_url)
    cursor.execute("SELECT ID FROM sitemaps WHERE TRIM(Url) = %s",(sitemap_url,))
    row = cursor.fetchone()

    if row:
        return row[0]

    cursor.execute("INSERT INTO sitemaps (Url) VALUES (%s)",(sitemap_url,))

    conn.commit()

    return cursor.lastrowid

def get_page_id(cursor,sitemap_id, url):
    cursor.execute("SELECT Id FROM sitemap_pages WHERE Sitemap_ID = %s AND Url = %s",(sitemap_id, url))
    row = cursor.fetchone()
    if row:
        return row[0]
    return None

def save_urls(cursor, conn, sitemap_id, urls):
    inserted = 0
    refreshed=0

    for url in urls:
        url = normalize_url(url)

        if url.lower().endswith(SKIP_EXTENSIONS):
            continue

        if url_exists(cursor,sitemap_id,url):
            refreshed += 1
            continue
            
            continue

        cursor.execute("INSERT INTO sitemap_pages (Sitemap_ID,Url) VALUES (%s,%s)" , (sitemap_id , url))

        inserted += 1

    conn.commit()

    logger.info(f"{inserted} new URLs inserted")
    logger.info(f"{refreshed} existing URLs refreshed")
    return inserted, refreshed

def get_all_sitemaps(cursor):
    cursor.execute("SELECT ID, Url FROM sitemaps ORDER BY ID DESC")
    return cursor.fetchall()

def get_urls_by_sitemap(cursor, sitemap_id):
    cursor.execute("SELECT Id, Url FROM sitemap_pages WHERE Sitemap_ID = %s ORDER BY Id", (sitemap_id,),)
    rows = cursor.fetchall()
    return [
        {
            "id": row[0],
            "url": row[1]
        }
        for row in rows
    ]

def get_page_content(cursor, page_id):
    cursor.execute("SELECT Id, Url, Page_Scrapped FROM sitemap_pages WHERE Id = %s", (page_id,))
    row = cursor.fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "url": row[1],
        "content": row[2]
    }

def get_all_scraped_pages(cursor):
    "Fetch all pages that have scraped content."
    cursor.execute("SELECT Id, Url, Page_Summary FROM sitemap_pages WHERE Page_Summary IS NOT NULL")
    rows = cursor.fetchall()
    return [
        {
            "id": row[0],
            "url": row[1],
            "content": row[2]
        }
        for row in rows
    ]

def get_pages_without_summary(cursor):
    cursor.execute("SELECT Id, Page_Scrapped FROM sitemap_pages WHERE Page_Scrapped IS NOT NULL AND Page_Summary IS NULL")
    return cursor.fetchall()