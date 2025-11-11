import os
import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from typing import List

# === KONFIGURASI ===
CHUNK_FOLDER = "./retrieval_results"  # lokasi file JSON berisi chunks
LABEL_OUTPUT_FOLDER = "./labeled_results"
os.makedirs(LABEL_OUTPUT_FOLDER, exist_ok=True)

# === INISIALISASI APP ===
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# === ROUTE: TAMPILKAN DAFTAR FILE ===
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    files = [f for f in os.listdir(CHUNK_FOLDER) if f.endswith(".json")]
    return templates.TemplateResponse("index.html", {"request": request, "files": files})

# === ROUTE: TAMPILKAN HALAMAN LABEL ===
@app.get("/label/{filename}", response_class=HTMLResponse)
async def label_file(request: Request, filename: str):
    file_path = os.path.join(CHUNK_FOLDER, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    return templates.TemplateResponse("label.html", {
        "request": request,
        "filename": filename,
        "chunks": chunks
    })

# === ROUTE: SIMPAN LABEL ===
@app.post("/submit/{filename}")
async def submit_labels(
    request: Request,
    filename: str,
    chunkid: List[str] = Form(...),
    text: List[str] = Form(...),
    filename_: List[str] = Form(...)
):
    form_data = await request.form()
    results = []
    for i in range(len(chunkid)):
        label_key = f"label_{i}"
        label = int(form_data.get(label_key, 0))  # default = 0 jika tidak dipilih
        results.append({
            "chunk_id": chunkid[i],
            "filename": filename_[i],
            "text": text[i],
            "label": label
        })

    out_path = os.path.join(LABEL_OUTPUT_FOLDER, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return RedirectResponse(f"/hasil/{filename}", status_code=302)

# === ROUTE: TAMPILKAN HASIL ===
@app.get("/hasil/{filename}", response_class=HTMLResponse)
async def hasil_label(request: Request, filename: str):
    output_path = os.path.join(LABEL_OUTPUT_FOLDER, filename)
    if not os.path.exists(output_path):
        return HTMLResponse(f"<h3>❌ Hasil untuk '{filename}' belum tersedia.</h3>", status_code=404)

    with open(output_path, "r", encoding="utf-8") as f:
        labeled_chunks = json.load(f)

    return templates.TemplateResponse("hasil.html", {
        "request": request,
        "filename": filename,
        "chunks": labeled_chunks
    })
