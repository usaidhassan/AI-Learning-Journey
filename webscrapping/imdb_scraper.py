from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.imdb.com/chart/top/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    )
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)


    page.wait_for_timeout(3000)


    for _ in range(10):
        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(1500)


    html = page.content()

    with open("imdb_page.html", "w", encoding="utf-8") as f:
        f.write(html)

    browser.close()

soup = BeautifulSoup(html, "lxml")

print("Page title:", soup.title.text)

movies = soup.select("li.ipc-metadata-list-summary-item")

print("Movies found:", len(movies))

data = []

for movie in movies:

    title_tag = movie.select_one(".ipc-title__text")
    title = title_tag.get_text(strip=True) if title_tag else None

    metadata = movie.select("li.ipc-inline-list__item")

    year = metadata[0].get_text(strip=True) if len(metadata) > 0 else None
    runtime = metadata[1].get_text(strip=True) if len(metadata) > 1 else None

    rating_tag = movie.select_one("span.ipc-rating-star--rating")
    rating = rating_tag.get_text(strip=True) if rating_tag else None

    votes_tag = movie.select_one("span.ipc-rating-star--voteCount")
    votes = votes_tag.get_text(strip=True) if votes_tag else None

    data.append({
        "Title": title,
        "Year": year,
        "Runtime": runtime,
        "Rating": rating,
        "Votes": votes
    })

df = pd.DataFrame(data)

print(df.head())
print(f"Total movies scraped: {len(df)}")

df.to_csv("imdb_top250.csv", index=False)

print("CSV saved successfully.")