from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

# Path to the file you want to serve for download
file_path = Path("/home/vadym_wsl/projects/Interior-Generation-Helper/web_app/sample_file.glb")


@app.get("/generate_room")
def generate_room(file: UploadFile = File(...)):
    return FileResponse(file_path, filename=file_path.name)




from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
from typing import List
from PIL import Image
import pytesseract

app = FastAPI()

# Function to perform OCR (Optical Character Recognition) on an image
def perform_ocr(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing OCR: {str(e)}")

# Endpoint to receive an image file and return text
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Check if the uploaded file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    # Save the uploaded image to the server
    with open(file.filename, "wb") as f:
        f.write(file.file.read())

    # Perform OCR on the saved image
    text_result = perform_ocr(file.filename)

    # Create a text file with the OCR result
    text_filename = file.filename.split(".")[0] + ".txt"
    with open(text_filename, "w") as text_file:
        text_file.write(text_result)

    # Return the text file as a response
    return PlainTextResponse(content=text_result, media_type="text/plain", filename=text_filename)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

