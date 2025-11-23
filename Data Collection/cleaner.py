import json
import re

INPUT_FILE = "all_movie_subs_daily_FIXED.json"
OUTPUT_FILE = "cleaned_movies.json"

def is_empty_text(t):
    if t is None:
        return True
    t = t.strip().lower()
    return (t == "" or t == "[removed]" or t == "[deleted]")

def looks_english(text):
    """Heuristic: text must contain mostly English letters/spaces."""
    english_chars = sum(c.isascii() for c in text)
    return english_chars / max(len(text), 1) > 0.7

deduped = {}

print("Loading raw data...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    raw = json.load(f)

print(f"Loaded {len(raw)} posts")

for p in raw:
    pid = p.get("id")
    if not pid:
        continue

    title = p.get("title", "").strip()
    text  = p.get("text", "").strip()

    # Skip empty posts entirely
    if title == "" and is_empty_text(text):
        continue

    # ENGLISH FILTER (optional, toggle this by uncommenting)
    # if not looks_english(title + " " + text):
    #     continue

    if pid not in deduped:
        deduped[pid] = p
    else:
        prev = deduped[pid]

        prev_text = prev.get("text", "")
        new_text  = text

        # If previous was removed and new is real, replace
        if is_empty_text(prev_text) and not is_empty_text(new_text):
            deduped[pid] = p

        # If both have text, keep the longer one (more complete)
        elif len(new_text) > len(prev_text):
            deduped[pid] = p

cleaned_list = list(deduped.values())
print(f"After dedupe: {len(cleaned_list)} posts remain")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_list, f, indent=2, ensure_ascii=False)

print(f"✔ Wrote cleaned dataset to {OUTPUT_FILE}")
