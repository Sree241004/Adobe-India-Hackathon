# Adobe India Hackathon 2025 – Challenge 1B

**Title:** Persona-Driven Document Intelligence  
**Team:** Sree241004  
**Solution:** Intelligent system to extract and rank relevant sections from PDFs using offline CPU-based processing.

---

## 🧠 Problem Summary
Build a smart system that:
- Reads a folder of PDFs
- Uses an input JSON defining a **persona** and their **job-to-be-done**
- Extracts relevant sections and refined text
- Ranks them based on importance
- Produces a structured output JSON

---

## 🧪 Test Case Collections

```
Collection 1/
├── PDFs/
├── challenge1b_input.json
├── challenge1b_output.json ← Generated

Collection 2/
├── PDFs/
├── challenge1b_input.json
├── challenge1b_output.json

Collection 3/
├── PDFs/
├── challenge1b_input.json
├── challenge1b_output.json
```

Each collection is processed independently.

---

## 🚀 How to Run (Docker)

### 1. Build the Docker Image

```bash
docker build -t challenge1b-solution .
```

### 2. Run the container (All collections)

```bash
docker run --rm -v "${PWD}:/app" challenge1b-solution
```

> On Windows PowerShell, use:
```powershell
docker run --rm -v "${PWD}:/app" challenge1b-solution
```

This will automatically:
- Process `Collection 1`, `Collection 2`, and `Collection 3`
- Create `challenge1b_output.json` inside each collection folder

---

## ⚙️ Tech Stack

- Python 3.10
- PyMuPDF for PDF parsing
- scikit-learn for text similarity
- TQDM for progress bar
- Docker for packaging

---

## 📁 Files

- `process_documents.py` — Main logic
- `Dockerfile` — Defines the environment
- `requirements.txt` — Python dependencies
- `approach_explanation.md` — Methodology writeup
- `README.md` — Usage and structure

---

## ✅ Output Format (JSON)

```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a 4-day trip",
    "processing_timestamp": "2025-07-27T13:00:00"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Things to Do in Nice",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "refined_text": "Nice is known for...",
      "page_number": 3
    }
  ]
}
```

---

## 🧊 Constraints

- Runs under 60 seconds
- Works offline (no internet)
- Model size under 1 GB
- CPU-only environment

---

## 👤 Authors

**Boga Sudharshini Sree**  
[sudharshinisree.boga@gmail.com]  
GitHub: [Sree241004]

**Palle Devi Sri Vinay Mohan Reddy**  
[iamvinaymohan@gmail.com]  
GitHub: [devisrivinay]

---
