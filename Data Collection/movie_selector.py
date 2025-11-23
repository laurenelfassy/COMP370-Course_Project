import json
import re

INPUT_FILE = "cleaned_movies.json"
OUTPUT_FILE = "filtered_four_movies.json"

# Movie keyword patterns (case-insensitive)
KEYWORDS = {
    "barbie": [
        r"\bbarbie\b",
        r"\bbarbenheimer\b",
        r"\bgreta gerwig\b"
    ],
    "oppenheimer": [
        r"\boppenheimer\b",
        r"\boppy\b",
        r"\bnolan\b"
    ],
    "mi": [
        r"\bmission impossible\b",
        r"\bmi7\b",
        r"\bdead reckoning\b",
        r"\btom cruise\b"
    ],
    "tmnt": [
        r"\btmnt\b",
        r"\bteenage mutant ninja turtles\b",
        r"\bmutant mayhem\b"
    ]
}

# Compile patterns for speed
COMPILED = {m: [re.compile(kw, re.IGNORECASE) for kw in kws] 
            for m, kws in KEYWORDS.items()}

def matches_any_movie(text):
    """Return True if text matches ANY movie keyword."""
    for movie, patterns in COMPILED.items():
        for pat in patterns:
            if pat.search(text):
                return True
    return False

print("Loading cleaned dataset...")
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

filtered = []

print("Filtering posts...")
for post in data:
    title = post.get("title", "")
    text  = post.get("text", "")
    combined = f"{title} {text}"

    if matches_any_movie(combined):
        filtered.append(post)

print(f"Kept {len(filtered)} posts out of {len(data)}")

print("Saving filtered dataset...")
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(filtered, f, indent=2, ensure_ascii=False)

print(f"✔ Saved {OUTPUT_FILE}")
