import requests
import json
import time
from datetime import datetime, timedelta, date, timezone

# CONFIG - scraped for subreddits with specific movie related title/content

SUBREDDITS = [
    "movies",
    "boxoffice",
    "film",
    "flicks"
]

# Set a start to end date (inclusive)   
START_DATE = date(2023, 7, 1)
END_DATE   = date(2023, 8, 10)

PAGE_SIZE = 100      # TRUE max output per call
OUTPUT_FILE = "all_movie_subs_daily_FIXED.json"

ENDPOINTS = [
    "https://api.pullpush.io/reddit/search/submission",
    "https://api.pushshift.io/reddit/search/submission"
]

# To avoid blacklisted IPs
HEADERS = {"User-Agent": "COMP370-movie-project"}


# Helper: try multiple endpoints
def try_request(params):
    for ep in ENDPOINTS:
        try:
            r = requests.get(ep, headers=HEADERS, params=params, timeout=15)
            if r.status_code == 200:
                return r
        except Exception:
            continue
    return None



# MAIN SCRAPER

def scrape_all_days():
    all_posts = []

    current = START_DATE
    while current <= END_DATE:
        print(f"\n==== {current} ====")

        start_dt = datetime(current.year, current.month, current.day, 0, 0, 0, tzinfo=timezone.utc)
        end_dt   = start_dt + timedelta(days=1)

        day_start_ts = int(start_dt.timestamp())
        day_end_ts   = int(end_dt.timestamp())

        for sub in SUBREDDITS:
            print(f"  Subreddit r/{sub}")

            # Timestamp-based pagination:
            after_ts = day_start_ts

            while True:
                params = {
                    "subreddit": sub,
                    "after": after_ts,
                    "before": day_end_ts,
                    "size": PAGE_SIZE,
                    "sort": "asc"
                }

                r = try_request(params)
                if not r:
                    print("    Request failed (skipping).")
                    break

                data = r.json().get("data", [])
                if not data:
                    print("    Reached final page.")
                    break

                print(f"    Fetched {len(data)} posts (after={after_ts})")

                # Save posts
                for post in data:
                    ts = post.get("created_utc")
                    readable = (
                        datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                        if ts else None
                    )

                    all_posts.append({
                        "subreddit": sub,
                        "id": post.get("id"),
                        "title": (post.get("title") or "").strip(),
                        "text": (post.get("selftext") or "").strip(),
                        "date": readable,
                        "created_utc": ts,
                        "permalink": post.get("permalink"),
                    })

                # Advance : NEW KEY STEP (the pages are not numbered on redit)
                last_ts = data[-1]["created_utc"]
                after_ts = last_ts + 1

                time.sleep(0.5)  # Polite delay

        current += timedelta(days=1)

    print(f"\nTotal posts scraped: {len(all_posts)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2, ensure_ascii=False)

    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape_all_days()
