from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import pytesseract
from PIL import Image
import shutil
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Luxury Invoice Extractor</title>
            <style>
                body { background-color: #f5f5f5; font-family: Arial, sans-serif; text-align: center; padding: 50px; }
                h1 { color: #333; font-size: 2.5em; margin-bottom: 20px; }
                form { background: white; padding: 40px; border-radius: 15px; display: inline-block; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
                input[type=file] { margin: 20px 0; }
                input[type=submit] { background: #000; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-size: 1em; cursor: pointer; }
                input[type=submit]:hover { background: #444; }
                pre { background: #eee; padding: 20px; border-radius: 10px; text-align: left; }
            </style>
        </head>
        <body>
            <h1>Luxury Invoice Extractor</h1>
            <form action="/extract" enctype="multipart/form-data" method="post">
                <input type="file" name="file" accept="image/*" required>
                <br>
                <input type="submit" value="Extract Invoice">
            </form>
        </body>
    </html>
    """

@app.post("/extract", response_class=HTMLResponse)
async def extract(file: UploadFile = File(...)):
    # save uploaded file temporarily
    temp_file = "temp.jpg"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # OCR
    text = pytesseract.image_to_string(Image.open(temp_file))

    # delete temp file
    os.remove(temp_file)

    # return result in HTML
    return f"""
    <html>
        <head>
            <title>Extracted Invoice</title>
            <style>
                body {{ background-color: #f5f5f5; font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
                h1 {{ color: #333; font-size: 2.5em; margin-bottom: 20px; }}
                pre {{ background: #eee; padding: 20px; border-radius: 10px; text-align: left; max-width: 800px; margin: auto; white-space: pre-wrap; word-wrap: break-word; }}
                a {{ display: inline-block; margin-top: 20px; text-decoration: none; color: #000; background: #ddd; padding: 10px 20px; border-radius: 8px; }}
                a:hover {{ background: #ccc; }}
            </style>
        </head>
        <body>
            <h1>Extracted Invoice</h1>
            <pre>{text}</pre>
            <a href="/">Upload Another Invoice</a>
        </body>
    </html>
    """
