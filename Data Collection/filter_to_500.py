import json
import random

INPUT_FILE = "filtered_four_movies.json"

OUT_500 = "sample_500.json"
OUT_200 = "open_coding_200.json"
OUT_300 = "annotation_300.json"

# Set seed for reproducibility
SEED = 42


def main():
    print("Loading filtered dataset...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Total movie-related posts: {len(data)}")

    if len(data) < 500:
        raise ValueError(
            f"You only have {len(data)} posts — need at least 500 for sampling."
        )

    # Shuffle randomly in place
    random.seed(SEED)
    random.shuffle(data)

    # Take first 500
    sample_500 = data[:500]

    # 200 for open coding
    open_200 = sample_500[:200]

    # 300 for annotation
    annot_300 = sample_500[200:]

    # Save all outputs
    print("Saving sample_500.json...")
    with open(OUT_500, "w", encoding="utf-8") as f:
        json.dump(sample_500, f, indent=2, ensure_ascii=False)

    print("Saving open_coding_200.json...")
    with open(OUT_200, "w", encoding="utf-8") as f:
        json.dump(open_200, f, indent=2, ensure_ascii=False)

    print("Saving annotation_300.json...")
    with open(OUT_300, "w", encoding="utf-8") as f:
        json.dump(annot_300, f, indent=2, ensure_ascii=False)

    print("✔ Sampling complete!")
    print("✔ 500 total in sample_500.json")
    print("✔ 200 in open_coding_200.json")
    print("✔ 300 in annotation_300.json")


if __name__ == "__main__":
    main()
