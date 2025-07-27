# Challenge 1B: Persona-Driven Document Intelligence — Approach Explanation

## 🧠 Problem Understanding
In this challenge, we were asked to build a system that behaves like a smart document analyst. It should:
- Read a collection of PDFs
- Understand the user persona and their task (job-to-be-done)
- Extract the most relevant content (titles + detailed text)
- Rank them based on how useful they are for the user’s task
- Return the result in a structured JSON format

We were provided with multiple collections of documents, each having:
- A set of PDFs
- A JSON file that defines the persona and their task

The goal was to build a solution that works **offline**, runs within **60 seconds**, and uses models under **1 GB**, using CPU-only.

---

## 🧩 Our Solution

### Step 1: Load Input JSON
For each collection folder, we load the `challenge1b_input.json` file. It contains:
- A list of documents (PDFs)
- A persona description (e.g., "Travel Planner")
- A job-to-be-done (e.g., "Plan a 4-day trip")

We combine the persona and job into one query string like:
> "Travel Planner needs to plan a 4-day trip"

This is our reference for relevance comparison.

---

### Step 2: Parse All PDFs
We use `PyMuPDF` (fitz) to read the text from each PDF page. For every page:
- We extract the **first line as section title**
- The rest is used as **raw content**
- Pages are stored along with filename and page number

---

### Step 3: Filter and Rank Sections
To improve quality:
- We ignore generic sections like "Introduction" or "Table of Contents"
- We prioritize sections with keywords (e.g., "cities", "tips", "experiences")

---

### Step 4: Similarity Matching
We use `TfidfVectorizer` and `cosine_similarity` from `scikit-learn`:
- Convert all page texts and query string into vector form
- Measure how close each page is to the persona’s task
- Combine similarity score + keyword priority to rank

---

### Step 5: Generate Output
- Top 5 most relevant sections are selected
- Metadata, ranked section titles, and refined full text are saved
- Final output is stored as `challenge1b_output.json` inside the collection

---

## 🧪 Why this works
Our solution is fast, lightweight, rule-augmented, and interpretable. It avoids heavy models and instead uses:
- Text vectorization
- Rule-based filtering
- PDF parsing
All under 60 seconds and under 1 GB.

This makes it ideal for CPU-only environments with no internet access.

---

## ✅ Tools & Libraries
- Python 3.10
- PyMuPDF (fitz)
- scikit-learn
- TQDM (for progress bar)
- Docker
