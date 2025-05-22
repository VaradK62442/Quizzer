from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
import string
from nltk.corpus import wordnet
import nltk

nltk.download('wordnet')

def preprocess(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    return text

def extract_keywords(text, max_keywords=5):
    words = preprocess(text).split()
    keywords = [w for w in words if w not in ENGLISH_STOP_WORDS]
    return keywords[:max_keywords]

def tfidf_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([text1, text2])
    score = cosine_similarity(vectors[0], vectors[1])[0, 0]
    return round(score, 2)

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower().replace('_', ' '))
    return synonyms

def keyword_match(keywords, user_text):
    user_words = set(preprocess(user_text).split())
    matches = []
    for kw in keywords:
        synonyms = get_synonyms(kw)
        synonyms.add(kw)
        matched = any(word in user_words for word in synonyms)
        matches.append((kw, matched))
    return matches

def highlight_keywords(keywords, user_text):
    words = user_text.split()
    highlighted = []
    lower_keywords = set(k.lower() for k in keywords)
    for w in words:
        if preprocess(w) in lower_keywords:
            highlighted.append(f"**{w}**")
        else:
            highlighted.append(w)
    return ' '.join(highlighted)

def mark_answer(correct_answer, user_answer, keyword_weight=0.4, semantic_weight=0.6):
    processed_correct = preprocess(correct_answer)
    processed_user = preprocess(user_answer)

    sim_score = tfidf_similarity(processed_correct, processed_user)
    
    keywords = extract_keywords(correct_answer)
    matches = keyword_match(keywords, user_answer)
    keyword_hits = sum(1 for _, matched in matches if matched)
    keyword_score = keyword_hits / len(keywords) if keywords else 0.0

    final_score = round((semantic_weight * sim_score + keyword_weight * keyword_score), 2)
    return final_score, matches

def main():
    answer = "Python is high-level programming language used for software development."
    user = "Python is used to create software and is a coding tool."
    score, matches = mark_answer(answer, user)
    
    print("Score:", score)
    print("Keyword Matches:")
    for kw, matched in matches:
        status = "YES" if matched else "NO"
        print(f"{kw}: {status}")
    highlighted_answer = highlight_keywords([kw for kw, _ in matches], user)
    print("Highlighted Answer:", highlighted_answer)

if __name__ == "__main__":
    main()

