# train_intent_classifier.py
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Sample questions
questions = [
    "I have NPK, pH, and rainfall. What crop should I grow?",
    "I’m from Maharashtra, what can I grow in Kharif?",
    "What crop should I plant after rice?",
]
labels = [1, 2, 3]  # Intent IDs for Model 1, 2, 3

# Train classifier
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)
clf = LogisticRegression().fit(X, labels)

# Save
joblib.dump(vectorizer, "intent_vectorizer.pkl")
joblib.dump(clf, "intent_classifier.pkl")
