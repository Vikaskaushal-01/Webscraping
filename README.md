# 📘 Wikipedia QA Bot

A clean, fast, and lightweight **Question Answering (QA) system** that scrapes Wikipedia articles, processes them, and retrieves the most relevant answer using **TF-IDF + Cosine Similarity**. Ideal for anyone exploring NLP, information retrieval, or building intelligent search tools.

---

## 🚀 Overview

This project demonstrates how to build a simple but effective QA engine:

* Scrape real Wikipedia articles
* Clean and preprocess text
* Break content into overlapping passages
* Use TF-IDF to convert text into searchable vectors
* Retrieve the best-matching answer to any user query

A great starter project for learning about search systems, NLP pipelines, and text analysis.

---

## ✨ Features

* 🌐 **Automated Wikipedia scraping** using Selenium + BeautifulSoup
* 🧹 **Robust text preprocessing** (cleaning, filtering, formatting)
* 📚 **Passage-based retrieval** for better accuracy
* 🧠 **TF-IDF vectorization** with cosine similarity ranking
* 💬 **Interactive CLI** — ask a question and get:

  * The best answer
  * The source article
  * The similarity score
* 🔎 Works fully offline after initial scraping

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/wiki-qa-bot.git
cd wiki-qa-bot
```

### 2. Install required dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Usage

### 1. Scrape Wikipedia pages

```bash
python scrape_wikipedia.py
```

This downloads and saves cleaned Wikipedia content locally.

### 2. Run the QA system

```bash
python simple_qa_tfidf.py
```

You can now type any question in the terminal and get:

* Answer snippet
* Source URL
* Similarity score

Example:

```
Q: What is Artificial Intelligence?
A: Artificial intelligence (AI) is the simulation of human intelligence in machines...
Source: https://en.wikipedia.org/wiki/Artificial_intelligence
Score: 0.82
```

---

## 📂 Repository Structure

| File/Folder                | Description                           |
| -------------------------- | ------------------------------------- |
| **scrape_wikipedia.py**    | Scrapes and saves Wikipedia articles  |
| **simple_qa_tfidf.py**     | Runs the question-answering pipeline  |
| **wikipedia_full_output/** | Stores scraped + cleaned article text |
| **test.py**                | Basic testing and demo functions      |

---

## 🧰 Technologies Used

* Python 3
* Selenium
* BeautifulSoup (bs4)
* scikit-learn (TF-IDF + cosine similarity)

---

## 🌟 Future Improvements (Optional Ideas)

* Replace TF-IDF with **Sentence-Transformers embeddings** for semantic search
* Build a **web UI** using Flask/FastAPI
* Add **FAISS** for large-scale vector search
* Add **PDF export** for Q&A sessions

---

## 🤝 Contributing

Contributions are welcome!
Feel free to open issues, suggest improvements, or submit pull requests.

---

#Python #NLP #WebScraping #MachineLearning #AI #QA
