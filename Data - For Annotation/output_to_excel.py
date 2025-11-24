import json
import pandas as pd
from pathlib import Path

# -------------------------------
# CONFIG
# -------------------------------
MOVIES = {
    "barbie": ["barbie", "greta gerwig", "margot robbie", "gosling", "barbenheimer"],
    "oppenheimer": ["oppenheimer", "nolan", "cillian", "oppen"],
    "mission_impossible": ["mission impossible", "mi7", "dead reckoning", "ethan hunt", "tom cruise"],
    "tmnt": ["tmnt", "mutant mayhem", "ninja turtles", "donatello", "raphael", "michelangelo"]
}

BASE = Path(__file__).parent   # Data – For Annotation folder

# Input files
OPEN_200_FILE = BASE / "open_coding_200.json"
SAMPLE_500_FILE = BASE / "sample_500.json"

# Output files
OUT_OPEN_200_XLSX = BASE / "open_coding_200.xlsx"
OUT_ANNOT_500_XLSX = BASE / "annotation_500.xlsx"


# -------------------------------
# HELPER: Determine which movie a post belongs to
# -------------------------------
def detect_movie(title, text):
    combined = (title + " " + text).lower()

    for movie, keywords in MOVIES.items():
        if any(k in combined for k in keywords):
            return movie
    return "unknown"


# -------------------------------
# BUILD OPEN CODING (200) EXCEL
# -------------------------------
def build_open_coding_excel():
    with open(OPEN_200_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    rows = []
    for p in posts:
        title = p.get("title", "")
        text = p.get("text", "")
        movie = detect_movie(title, text)

        rows.append({
            "title": title,
            "text": text,
            "movie": movie,
            "round1": "",
            "round2": "",
            "round3": ""
        })

    df = pd.DataFrame(rows)
    df.to_excel(OUT_OPEN_200_XLSX, index=False)

    print(f"✔ Created {OUT_OPEN_200_XLSX.name}")


# -------------------------------
# BUILD FINAL ANNOTATION (500) EXCEL
# -------------------------------
def build_annotation_500_excel():
    with open(SAMPLE_500_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    rows = []
    for p in posts:
        title = p.get("title", "")
        text = p.get("text", "")
        movie = detect_movie(title, text)

        rows.append({
            "title": title,
            "text": text,
            "movie": movie,
            "final_annotation": ""
        })

    df = pd.DataFrame(rows)
    df.to_excel(OUT_ANNOT_500_XLSX, index=False)

    print(f"✔ Created {OUT_ANNOT_500_XLSX.name}")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    print("Building Excel files...")
    build_open_coding_excel()
    build_annotation_500_excel()
    print("✔ All done.")
