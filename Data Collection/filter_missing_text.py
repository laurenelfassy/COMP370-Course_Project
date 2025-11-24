import json
from langdetect import detect, LangDetectException

INPUT_FILE = "../Data - Larger Sample/filtered_four_movies.json"
OUTPUT_VALID = "../Data - Larger Sample/filtered_four_movies_VALID.json"
OUTPUT_DROPPED = "../Data - Larger Sample/dropped_posts.json"


def is_english(text):
    try:
        return detect(text) == "en"
    except LangDetectException:
        return False


def is_empty_or_removed(text):
    if text is None:
        return True
    t = text.strip().lower()
    return t == "" or t == "[deleted]" or t == "[removed]"


def contains_link(text):
    t = text.lower()
    return ("http://" in t) or ("https://" in t)


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    clean = []
    dropped = []

    for post in data:
        title = post.get("title", "").strip()
        text = post.get("text", "").strip()
        combined = (title + " " + text).strip()

        # --- DROP CASES ---
        if is_empty_or_removed(title) or is_empty_or_removed(text):
            dropped.append(post)
            continue

        if contains_link(title) or contains_link(text):
            dropped.append(post)
            continue

        if not is_english(combined):
            dropped.append(post)
            continue

        # --- KEEP ---
        clean.append(post)

    # --- SAVE ---
    with open(OUTPUT_VALID, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2, ensure_ascii=False)

    with open(OUTPUT_DROPPED, "w", encoding="utf-8") as f:
        json.dump(dropped, f, indent=2, ensure_ascii=False)

    print(f"✔ Kept {len(clean)} posts")
    print(f"✔ Dropped {len(dropped)} posts")


if __name__ == "__main__":
    main()
