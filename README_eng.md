#  FastAPI Labeling Tool for Retrieval Results

This project is a **web-based labeling tool** built using **FastAPI** and **Jinja2** templates.
It allows users to load retrieval result files (`.json`), review text chunks, and assign labels such as **relevant** or **not relevant**.
All labeled results are stored automatically for later use in model evaluation or training datasets.

---

##  Project Structure

```
your_project/
├── retrieval_results/       # Folder containing input JSON retrieval results
│   ├── retrieval_apbd.json
│   └── retrieval_pajak.json
├── labeled_results/         # Folder where labeled outputs are saved
├── templates/               # HTML templates for FastAPI (Jinja2)
│   ├── index.html
│   ├── label.html
│   └── hasil.html
├── static/                  # (Optional) Static assets like CSS/JS
└── labeling_tool.py         # Main FastAPI application
```

---

##  Requirements

Install dependencies before running the app:

```bash
pip install fastapi uvicorn jinja2 starlette
```

Optional (for monitoring/logging):

```bash
pip install python-multipart
```

---

##  How to Run

Run the FastAPI app locally using **Uvicorn**:

```bash
uvicorn labeling_tool:app --reload --port 8000
```

Then open your browser at:
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

##  How It Works

1. **Homepage (`/`)**
   Displays a list of available `.json` files inside the `retrieval_results/` folder.

2. **Labeling Page (`/label/{filename}`)**
   Loads the content of the selected file and presents each chunk with two labeling options:

   * ✅ Relevant (value `1`)
   * ❌ Not Relevant (value `0`)

3. **Submit Labels (`/submit/{filename}`)**
   Saves the labeling results into the `labeled_results/` directory as a JSON file with the same filename.

4. **View Results (`/hasil/{filename}`)**
   Displays all labeled chunks with their assigned labels.

---

##  Template Overview

### **index.html**

Displays a list of JSON files available for labeling.

### **label.html**

Form-based interface to review and label text chunks interactively.

### **hasil.html**

Shows the saved labeling results after submission.

---

##  Example JSON Structure

Each input JSON file (e.g., `retrieval_apbd.json`) should contain a list of chunks with these fields:

```json
[
  {
    "chunk_id": "chunk_001",
    "filename": "apbd.txt",
    "text": "Pemerintah daerah menetapkan anggaran berdasarkan kebutuhan publik..."
  },
  {
    "chunk_id": "chunk_002",
    "filename": "apbd.txt",
    "text": "Laporan realisasi anggaran menunjukkan peningkatan pada sektor pendidikan..."
  }
]
```

After labeling, the output will look like this:

```json
[
  {
    "chunk_id": "chunk_001",
    "filename": "apbd.txt",
    "text": "Pemerintah daerah menetapkan anggaran berdasarkan kebutuhan publik...",
    "label": 1
  },
  {
    "chunk_id": "chunk_002",
    "filename": "apbd.txt",
    "text": "Laporan realisasi anggaran menunjukkan peningkatan pada sektor pendidikan...",
    "label": 0
  }
]
```

---

## 💡 Notes

* You can customize the label values or add more label types (e.g., `neutral`, `uncertain`) by modifying the radio button section in `label.html`.
* The app supports CORS, so it can be integrated with other front-end or dashboard systems.
* Folder paths (`CHUNK_FOLDER` and `LABEL_OUTPUT_FOLDER`) can be adjusted directly in `labeling_tool.py`.

---

## 📜 License

This project is released under the **MIT License**.
Feel free to modify and use it for your research, annotation projects, or dataset preparation.

---
