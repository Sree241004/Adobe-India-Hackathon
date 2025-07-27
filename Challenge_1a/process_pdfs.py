import os
import json
import re
import unicodedata
import time
from pathlib import Path
import fitz  # PyMuPDF
from collections import defaultdict

MAX_PAGES = None  # Set to an integer like 50 to limit processing to first N pages

def extract_title(doc):
    page = doc[0]
    blocks = [b for b in page.get_text("dict")["blocks"] if b.get("type", 0) == 0]
    largest_size = 0
    title_candidates = []

    for b in blocks:
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                if s["size"] > largest_size:
                    largest_size = s["size"]

    for b in blocks:
        for l in b.get("lines", []):
            line_text = ""
            max_size = 0
            for s in l.get("spans", []):
                line_text += s["text"].strip() + " "
                max_size = max(max_size, s["size"])
            if line_text.strip() and abs(max_size - largest_size) < 0.1:
                title_candidates.append(line_text.strip())

    return " ".join(title_candidates).strip()

def is_cjk(text):
    return any('CJK' in unicodedata.name(char, '') for char in text)

def extract_headings(doc, title_to_exclude):
    font_sizes = defaultdict(int)
    all_lines = []
    norm_title = title_to_exclude.strip().lower()

    for page_num, page in enumerate(doc):
        if MAX_PAGES and page_num >= MAX_PAGES:
            break

        blocks = [b for b in page.get_text("dict")["blocks"] if b.get("type", 0) == 0]
        for b in blocks:
            for l in b.get("lines", []):
                line_text = ""
                max_size = 0
                for s in l.get("spans", []):
                    line_text += s["text"].strip() + " "
                    font_sizes[s["size"]] += 1
                    max_size = max(max_size, s["size"])

                text = line_text.strip()
                if not text or text.lower() == norm_title:
                    continue

                all_lines.append({
                    "text": text,
                    "size": max_size,
                    "page": page_num
                })

    sorted_sizes = sorted(font_sizes.items(), key=lambda x: (-x[0], -x[1]))
    size_map = {}
    for i, (size, _) in enumerate(sorted_sizes[:4]):
        size_map[f"H{i+1}"] = size

    def heading_level(text, size):
        if size >= size_map.get("H1", 16):
            return "H1"
        elif size >= size_map.get("H2", 13):
            return "H2"
        elif size >= size_map.get("H3", 11):
            return "H3"
        elif size >= size_map.get("H4", 9):
            return "H4"

        num_match = re.match(r"^(\d+(\.\d+)*\.?)", text)
        if num_match:
            depth = text.count(".")
            return ["H1", "H2", "H3", "H4"][min(depth, 3)]

        if is_cjk(text):
            return "H2" if len(text) > 2 else "H3"

        return None

    outline = []
    for entry in all_lines:
        level = heading_level(entry["text"], entry["size"])
        if level and len(entry["text"]) > 1:
            outline.append({
                "level": level,
                "text": entry["text"].strip(),
                "page": entry["page"]
            })

    return outline

def process_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = list(input_dir.glob("*.pdf"))

    for pdf_file in pdf_files:
        start = time.time()
        try:
            doc = fitz.open(str(pdf_file))
            title = extract_title(doc)
            outline = extract_headings(doc, title)

            output_data = {
                "title": title,
                "outline": outline
            }

            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            duration = time.time() - start
            print(f"[✓] Processed {pdf_file.name} → {output_file.name} ({duration:.2f}s)")
        except Exception as e:
            print(f"[✗] Failed to process {pdf_file.name}: {e}")

if __name__ == "__main__":
    print("🚀 Starting multilingual PDF processing")
    process_pdfs()
    print("✅ Completed processing PDFs")