# FileTransmit.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
import os
import zipfile
import io
from datetime import datetime
from typing import List

file_transmit_router = APIRouter()

# Define the workspace directory
WORKSPACE_FOLDER = './'
if not os.path.exists(WORKSPACE_FOLDER):
    os.makedirs(WORKSPACE_FOLDER)

@file_transmit_router.post('/upload')
async def upload_file(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files selected for uploading")

    for file in files:
        if file.filename == '':
            continue
        file_location = os.path.join(WORKSPACE_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

    return JSONResponse(content={"message": "Files uploaded successfully"})

# Example endpoint to download a file
@file_transmit_router.get('/download/{filename}')
async def download_file(filename: str):
    file_path = os.path.join(WORKSPACE_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, filename=filename)

# Example endpoint to download a zip of all files
@file_transmit_router.get('/download_all')
async def download_all_files():
    zip_filename = f"all_files_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_path = os.path.join(WORKSPACE_FOLDER, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(WORKSPACE_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, WORKSPACE_FOLDER))
    
    return FileResponse(path=zip_path, filename=zip_filename)