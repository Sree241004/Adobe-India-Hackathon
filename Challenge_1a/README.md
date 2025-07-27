
# PDF Title and Outline Extractor (Adobe Hackathon Challenge 1a)

This project is a Dockerized solution to process PDF files and extract structured data — including the document title and hierarchical headings (H1, H2, H3). It supports multilingual PDFs (e.g. English, Telugu, Japanese) and outputs results as JSON files conforming to a specific schema.

---

## 🚀 Features

- ✅ Extracts the **document title** (largest text on the first line of first page)
- ✅ Detects **headings** by analyzing font size (H1, H2, H3, H4)
- ✅ Processes **multilingual PDFs** (English, Telugu, Japanese, etc.)
- ✅ Outputs structured data as `.json` files
- ✅ Fully containerized with Docker
- ✅ Compatible with **amd64 architecture** and **offline execution**

---

## 📁 Project Structure

```
Challenge_1a/
├── sample_dataset/
│   ├── pdfs/           # Input PDF files (read-only)
│   ├── outputs/        # Generated JSON output
│   └── schema/
│       └── output_schema.json
├── process_pdfs.py     # Main PDF processor script
├── Dockerfile          # Container configuration
└── README.md           # This file
```

---

## 🧰 Technologies Used

- Python 3.10
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)
- reportlab (for PDF testing)
- json
- Docker

---

## 🐳 Build & Run with Docker

### 🔨 Build the Docker image:

```bash
docker build --platform linux/amd64 -t pdf-processor .
```

### ▶️ Run the container:

```bash
docker run --rm   -v "$(pwd)/sample_dataset/pdfs:/app/input:ro"   -v "$(pwd)/sample_dataset/outputs:/app/output"   --network none pdf-processor
```

> ⚠️ Windows PowerShell users: Replace `$(pwd)` with `${PWD}` or provide the full path.

---

## 📥 Input

- Place `.pdf` files inside `sample_dataset/pdfs`
- PDF structure must contain a valid title and heading-style text

---

## 📤 Output

- `.json` files will be generated in `sample_dataset/outputs`
- Output structure conforms to `sample_dataset/schema/output_schema.json`

Example output:
```json
{
  "title": "తెలుగు భాష పై పరిచయం",
  "outline": [
    {
      "level": "H1",
      "text": "భాష యొక్క చరిత్ర ",
      "page": 0
    }
  ]
}
```

---

## ✅ Constraints Handled

- 🕒 Under 10 seconds for 50-page PDFs
- 📦 Model size: None / <200MB (no ML model used)
- 🌐 No internet access at runtime
- 🧠 Works fully on CPU (no GPU)
- 🧱 Platform: linux/amd64

---

## 🧪 Testing

You can test the system with multilingual files including:
- English
- Telugu
- Hindi

A sample 50-page Telugu PDF is available in `sample_dataset/pdfs/telugu_sample_50_pages.pdf` *(or add your own)*

---

## 📄 Schema

Ensure output matches `sample_dataset/schema/output_schema.json`. This includes:
- `title` (string)
- `outline` (list of `{level, text, page}`)

---

## 👤 Authors

**Boga Sudharshini Sree**  
[sudharshinisree.boga@gmail.com]  
GitHub: [Sree241004]

**Palle Devi Sri Vinay Mohan Reddy**  
[iamvinaymohan@gmail.com]  
GitHub: [devisrivinay]

---

