DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "tannu@DBMS",
    "database": "work"
}

REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
BATCH_SIZE = 10

HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
}

REMOVE_TAGS = ["script", "style", "noscript"]

SKIP_EXTENSIONS = (".pdf",".jpg",".jpeg",".png",".gif",".svg",".zip",".xml",".doc",".docx",".xls",".xlsx",".ppt",".pptx")

LOG_FOLDER = "logs"
LOG_FILE = "logs/scraper.log"
LOG_LEVEL = "INFO"