from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def clean_word(word):
    return word.lower().strip(".,!?;:()[]{}\"'")


def get_query_words(query):
    words = query.split()
    clean_words = []

    for word in words:
        cleaned = clean_word(word)

        if len(cleaned) > 2:
            clean_words.append(cleaned)

    return clean_words


def read_documents():
    documents = []

    for file_path in DATA_DIR.glob("*.md"):
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        document = {
            "source": str(file_path.relative_to(BASE_DIR)),
            "text": text
        }

        documents.append(document)

    return documents


def score_document(query_words, document_text):
    score = 0
    lower_text = document_text.lower()

    for word in query_words:
        if word in lower_text:
            score = score + 1

    return score


def search_documents(query, max_results=3):
    query_words = get_query_words(query)
    documents = read_documents()
    results = []

    for document in documents:
        score = score_document(query_words, document["text"])

        if score > 0:
            result = {
                "source": document["source"],
                "score": score,
                "text": document["text"][:1200]
            }

            results.append(result)

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:max_results]


def make_context_text(results):
    if not results:
        return "No local travel notes were found."

    context_parts = []

    for result in results:
        part = f"""
Source: {result["source"]}
Content:
{result["text"]}
"""
        context_parts.append(part)

    return "\n---\n".join(context_parts)
