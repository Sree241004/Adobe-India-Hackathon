FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY process_pdfs.py .

# Preinstall required packages (at build time, internet is allowed)
RUN pip install --no-cache-dir pymupdf

CMD ["python", "process_pdfs.py"]
