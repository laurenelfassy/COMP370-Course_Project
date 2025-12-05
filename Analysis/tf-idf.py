import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud


df = pd.read_excel('../Data - For Annotation/annotated_500.xlsx')

df['final_annotation'] = df['final_annotation'].replace({
    "MARKETING_HYPE": "INDUSTRY_STRATEGY"
})
df['combined'] = (df['title'] + '. ' + df['text']).str.lower()

for topic in df['final_annotation'].unique():
    # Filter rows for this topic
    sub_df = df[df['final_annotation'] == topic]

    # Clean filename (remove spaces, special chars
    safe_topic = str(topic).replace(" ", "_")

    # Save to CSV
    sub_df.to_csv(f"topic_{safe_topic}.csv", index=False)

    print(f"Saved: topic_{safe_topic}.csv")


df['combined'] = df['combined'].str.replace(r'\bmovie\b|\bmovies\b|\blike\b|\bjust\b|\bfilm\b', '', regex=True)


topic_docs = df.groupby('final_annotation')['combined'].apply(lambda x: ' '.join(x))

# 3️⃣ Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)

# 4️⃣ Fit and transform the topic documents
tfidf_matrix = vectorizer.fit_transform(topic_docs)

# 5️⃣ Get the words (features)
feature_names = vectorizer.get_feature_names_out()

# 6️⃣ Convert TF-IDF matrix to DataFrame for easy handling
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index=topic_docs.index, columns=feature_names)

top_words = {}
for topic in tfidf_df.index:
    sorted_words = tfidf_df.loc[topic].sort_values(ascending=False)
    top_words[topic] = sorted_words.head(10)

# Print top TF-IDF words
for topic, series in top_words.items():
    print(f"🧩 Topic: {topic}")
    for word, value in series.items():
        print(f"{word}")
    print()


# Compute word count and character count for each post
df['word_count'] = df['combined'].apply(lambda x: len(x.split()))
df['char_count'] = df['combined'].apply(len)

length_stats = df.groupby('final_annotation').agg(
    avg_words=('word_count', 'mean'),
    median_words=('word_count', 'median'),
    avg_chars=('char_count', 'mean'),
    count=('combined', 'count')
).sort_values('avg_words', ascending=False)

print(length_stats)


# ----------------------------
# N-GRAMS
# ----------------------------
def get_top_ngrams(corpus, ngram_range=(2,3), top_n=10):
    vectorizer = CountVectorizer(ngram_range=ngram_range, stop_words='english')
    X = vectorizer.fit_transform(corpus)
    sums = X.sum(axis=0)
    ngram_counts = [(ngram, sums[0, idx]) for ngram, idx in vectorizer.vocabulary_.items()]
    ngram_counts = sorted(ngram_counts, key=lambda x: x[1], reverse=True)
    return ngram_counts[:top_n]

topic_ngrams = {}
for topic, group in df.groupby('final_annotation'):
    corpus = group['combined'].tolist()
    topic_ngrams[topic] = get_top_ngrams(corpus, ngram_range=(2,3), top_n=10)

# Export LaTeX tables
latex_tables = ""
for topic, ngrams in topic_ngrams.items():
    latex_tables += f"\\begin{{table}}[h]\n\\centering\n"
    latex_tables += f"\\caption{{Top 10 n-grams for topic: {topic}}}\n"
    latex_tables += "\\begin{tabular}{lr}\n\\hline\n"
    latex_tables += "N-gram & Count \\\\\n\\hline\n"
    for phrase, count in ngrams:
        latex_tables += f"{phrase} & {count} \\\\\n"
    latex_tables += "\\hline\n\\end{tabular}\n\\end{table}\n\n"

with open("topic_ngrams.tex", "w", encoding="utf-8") as f:
    f.write(latex_tables)

print("LaTeX tables saved to topic_ngrams.tex")


# ----------------------------
# PIE CHART
# ----------------------------
topic_counts = df['final_annotation'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(
    topic_counts.values,
    labels=topic_counts.index,
    autopct='%1.1f%%',
    startangle=90
)

plt.title("Topic Distribution in 500 Annotated Posts")
plt.tight_layout()
plt.savefig("topic_distribution.png", dpi=600)
plt.show()

fig, axes = plt.subplots(3, 3, figsize=(16, 12))

for (topic, words), ax in zip(top_words.items(), axes.flatten()):
    wc = WordCloud(
        width=600,
        height=400,
        background_color="white"
    ).generate_from_frequencies(words)

    ax.imshow(wc, interpolation="bilinear")
    ax.set_title(topic, fontsize=20, fontweight='bold')
    ax.axis("off")

plt.tight_layout()
plt.savefig("tfidf_wordclouds.pdf", dpi=800)
plt.show()