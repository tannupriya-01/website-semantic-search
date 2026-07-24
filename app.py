import re
from fastapi import Query
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import WebsiteRequest , SearchRequest
from scraper import process_website
from embeddings.search import semantic_search
from database import (get_connection, get_all_sitemaps ,get_urls_by_sitemap , get_page_content)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "FastAPI is working!"}


@app.post("/scrape")
def scrape(request: WebsiteRequest):
    result = process_website(request.website)
    return result

@app.get("/sitemaps")
def fetch_sitemaps():
    conn, cursor = get_connection()

    try:
        rows = get_all_sitemaps(cursor)
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "url": row[1]
            })
        return result

    finally:
        cursor.close()
        conn.close()

@app.get("/sitemaps/{sitemap_id}/urls")
def get_sitemap_urls(sitemap_id: int):
    conn, cursor = get_connection()

    try:
        urls = get_urls_by_sitemap(cursor, sitemap_id)
        return urls

    finally:
        cursor.close()
        conn.close()

@app.get("/pages/{page_id}")
def fetch_page(page_id: int):
    conn, cursor = get_connection()

    try:
        page = get_page_content(cursor, page_id)
        if page is None:
            return {"error": "Page not found"}
        return page

    finally:
        cursor.close()
        conn.close()

@app.post("/semantic-search")
def search(request: SearchRequest):

    results = semantic_search(request.query)

    return {
        "query": request.query,
        "results": results
    }

@app.get("/suggest")
def suggest(q: str = Query(...)):
    conn, cursor = get_connection()

    try:
        cursor.execute("SELECT Page_Scrapped FROM sitemap_pages WHERE Page_Scrapped IS NOT NULL")
        rows = cursor.fetchall()
        suggestions = set()
        query = q.lower()

        for row in rows:

            text = row[0]

            if not text:
                continue

            sentences = re.split(r"[.!?\n]", text)

            for sentence in sentences:

                sentence = sentence.strip()

                if not sentence:
                    continue

                lower_sentence = sentence.lower()

                if query in lower_sentence:

                    words = sentence.split()

                    for i, word in enumerate(words):

                        clean_word = re.sub(r"[^a-zA-Z0-9]", "", word).lower()

                        if clean_word.startswith(query):

                            phrase = " ".join(words[i:i+3])
                            suggestions.add(phrase)
                            break

                if len(suggestions) >= 10:
                    break

            if len(suggestions) >= 10:
                break

        return {
            "suggestions": sorted(suggestions)
        }

    finally:
        cursor.close()
        conn.close()