import os
import json
import fitz  # PyMuPDF
import datetime
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_pages(doc_path):
    doc = fitz.open(doc_path)
    pages = []
    for page in doc:
        text = page.get_text().strip()
        pages.append(text)
    return pages

def clean(text):
    return re.sub(r"\s+", " ", text.strip())

def process_collection(collection_path):
    input_json_path = os.path.join(collection_path, "challenge1b_input.json")
    output_json_path = os.path.join(collection_path, "challenge1b_output.json")
    pdf_dir = os.path.join(collection_path, "PDFs")

    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    job_text = data["job_to_be_done"]["task"]
    persona_text = data["persona"]["role"]
    combined_query = f"{persona_text} needs to {job_text}"

    documents = data["documents"]
    all_sections = []

    for doc_meta in documents:
        file_path = os.path.join(pdf_dir, doc_meta["filename"])
        if not os.path.exists(file_path):
            print(f"⚠️ Skipping missing file: {file_path}")
            continue

        pages = extract_pages(file_path)
        for i, text in enumerate(pages):
            section_title = text.strip().split('\n')[0][:80]
            all_sections.append({
                "document": doc_meta["filename"],
                "page_number": i + 1,
                "section_title": section_title,
                "raw_text": clean(text)
            })

    ignore_titles = {"conclusion", "introduction", "table of contents", ""}
    priority_keywords = [
        "cities", "things to do", "cuisine", "packing", "tips",
        "nightlife", "activities", "adventures", "experiences", "travel"
    ]

    filtered_sections = []
    for sec in all_sections:
        title = sec["section_title"].lower()
        if title.strip() in ignore_titles or title.strip() == "":
            continue
        priority_score = sum(kw in title for kw in priority_keywords)
        sec["priority_score"] = priority_score
        filtered_sections.append(sec)

    texts = [s["raw_text"] for s in filtered_sections]
    texts.append(combined_query)

    vectorizer = TfidfVectorizer().fit_transform(texts)
    vectors = vectorizer.toarray()

    query_vec = vectors[-1]
    content_vecs = vectors[:-1]

    sims = cosine_similarity([query_vec], content_vecs)[0]
    for idx, sim in enumerate(sims):
        filtered_sections[idx]["score"] = sim + filtered_sections[idx]["priority_score"]

    top_sections = sorted(filtered_sections, key=lambda x: -x["score"])[:5]

    extracted_sections = []
    subsection_analysis = []

    for rank, sec in enumerate(top_sections, 1):
        extracted_sections.append({
            "document": sec["document"],
            "section_title": sec["section_title"],
            "importance_rank": rank,
            "page_number": sec["page_number"]
        })
        subsection_analysis.append({
            "document": sec["document"],
            "refined_text": sec["raw_text"],
            "page_number": sec["page_number"]
        })

    result = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": persona_text,
            "job_to_be_done": job_text,
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"✅ Processed {collection_path} → Output saved to challenge1b_output.json")

def main():
    base_dir = os.getcwd()
    for name in os.listdir(base_dir):
        if name.lower().startswith("collection"):
            collection_path = os.path.join(base_dir, name)
            if os.path.isdir(collection_path):
                try:
                    process_collection(collection_path)
                except Exception as e:
                    print(f"❌ Failed to process {collection_path}: {e}")

if __name__ == "__main__":
    main()
