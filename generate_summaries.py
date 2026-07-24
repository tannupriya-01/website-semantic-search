from concurrent.futures import ThreadPoolExecutor, as_completed
from database import (
    get_connection,
    get_pages_without_summary,
    update_page_summary
)

from summary_generator import generate_summary

def process_page(page):

    page_id, content = page
    conn, cursor = get_connection()

    try:
        summary = generate_summary(content)
        update_page_summary(
            cursor,
            conn,
            page_id,
            summary
        )
        return page_id, "Success"

    except Exception as e:
        return page_id, f"Error: {e}"

    finally:
        cursor.close()
        conn.close()

def main():

    conn, cursor = get_connection()
    rows = get_pages_without_summary(cursor)
    print(f"Found {len(rows)} pages")
    cursor.close()
    conn.close()

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(process_page, page)
            for page in rows
        ]

        completed = 0
        for future in as_completed(futures):

            completed += 1
            page_id, status = future.result()
            print(f"[{completed}/{len(rows)}] Page {page_id}: {status}")

if __name__ == "__main__":
    main()