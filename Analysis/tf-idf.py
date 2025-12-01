import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re



df = pd.read_excel('../Data - For Annotation/annotated_500.xlsx')


df['combined'] = (df['title'] + ' ' + df['text']).str.lower()
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

# 7️⃣ Extract top 10 words per topic
top_words = {}
for topic in tfidf_df.index:
    sorted_words = tfidf_df.loc[topic].sort_values(ascending=False)
    top_words[topic] = sorted_words.head(10).index.tolist()

# 8️⃣ Display results
for topic, words in top_words.items():
    print(f"🧩 Topic: {topic}")
    print(", ".join(words))
    print()
