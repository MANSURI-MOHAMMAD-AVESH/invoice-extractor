from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from PIL import Image
import pytesseract
import shutil
import re

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <h1>Invoice Extractor API</h1>
    <p>Go to <a href='/docs'>/docs</a> to use the API</p>
    """

def extract_invoice_fields(text):
    invoice_number = re.search(r'Invoice Number[: ]+(\d+)', text)
    date = re.search(r'Date[: ]+([0-9/-]+)', text)
    total = re.search(r'Total[: ]+\$?([0-9,.]+)', text)
    vendor = re.search(r'From[: ]+(.*)', text)

    return {
        "invoice_number": invoice_number.group(1) if invoice_number else None,
        "date": date.group(1) if date else None,
        "total": total.group(1) if total else None,
        "vendor": vendor.group(1) if vendor else None
    }

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    with open("temp.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    img = Image.open("temp.jpg")
    text = pytesseract.image_to_string(img)
    data = extract_invoice_fields(text)
    
    return data
