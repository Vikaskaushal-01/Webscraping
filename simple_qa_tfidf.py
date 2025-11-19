# simple_qa_tfidf.py
# TF-IDF based simple QA over the scraped files

import re, textwrap
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = Path("wikipedia_full_output")
PASSAGE_CHARS = 400
PASSAGE_STRIDE = 200
TOP_K_PASSAGES = 3

if not DATA_DIR.exists() or not any(DATA_DIR.glob("*_full.txt")):
    raise FileNotFoundError(f"No '*_full.txt' files in {DATA_DIR}. Run scraper first.")

def load_docs(folder):
    files = sorted(folder.glob("*_full.txt"))
    docs = []
    for p in files:
        txt = p.read_text(encoding="utf-8")
        docs.append((p.name, txt))
    return docs

def make_passages(text, size=PASSAGE_CHARS, stride=PASSAGE_STRIDE):
    t = re.sub(r"\s+", " ", text).strip()
    if len(t) <= size:
        return [t]
    parts, start = [], 0
    L = len(t)
    while start < L:
        end = min(start+size, L)
        parts.append(t[start:end].strip())
        if end == L:
            break
        start += stride
    return parts

docs = load_docs(DATA_DIR)
passages = []
meta = []
for name, txt in docs:
    pgs = make_passages(txt)
    for i, p in enumerate(pgs):
        passages.append(p)
        meta.append({"doc": name, "passage_id": i})

print("Passages:", len(passages))

vectorizer = TfidfVectorizer(stop_words="english", max_df=0.9)
tfidf = vectorizer.fit_transform(passages)
print("TF-IDF matrix shape:", tfidf.shape)

def split_sentences(text):
    sents = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sents if s.strip()]

def answer_question(question):
    qvec = vectorizer.transform([question])
    sims = cosine_similarity(qvec, tfidf)[0]
    top_idx = sims.argsort()[::-1][:TOP_K_PASSAGES]
    best_idx = top_idx[0]
    best_passage = passages[best_idx]
    m = meta[best_idx]
    sents = split_sentences(best_passage)
    if not sents:
        return {"answer": best_passage[:800], "source": m["doc"], "snippet": best_passage}
    sent_vecs = vectorizer.transform(sents)
    sent_sims = cosine_similarity(qvec, sent_vecs)[0]
    best_sent_idx = sent_sims.argmax()
    best_sentence = sents[best_sent_idx]
    return {"answer": best_sentence, "source": m["doc"], "snippet": best_passage, "scores": {"passage": float(sims[best_idx]), "sentence": float(sent_sims[best_sent_idx])}}

print("Simple TF-IDF QA ready. Type questions (Ctrl+C to quit).")
while True:
    try:
        q = input("\nQuestion: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        break
    if not q:
        continue
    res = answer_question(q)
    print("\nAnswer:\n", textwrap.fill(res["answer"], width=90))
    print("\nSource:", res["source"])
    print("Snippet:\n", textwrap.shorten(res["snippet"], width=400))
    if "scores" in res:
        sc = res["scores"]; print(f"Scores -> passage: {sc['passage']:.4f}, sentence: {sc['sentence']:.4f}")
