from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from typing import List
import pandas as pd
import csv
from fastapi.middleware.cors import CORSMiddleware

#This setup allows you to upload files, check their existence, and 
#access them via URLs in the static/files directory.

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")
# Mounts the directory named "static" so files in this directory can be accessed via /static

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
# Adds middleware to allow requests from any origin (e.g., different websites or servers).

# Ensure the directory exists
UPLOAD_DIRECTORY = "static/files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Ensure the directory exists
UPLOAD_DIRECTORY = "static/files"
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.post("/files/")
async def get_files(filenames: List[str] = Body(...)):
    file_paths = []
    for filename in filenames:
        file_path = f"{UPLOAD_DIRECTORY}/{filename}"
        if os.path.exists(file_path):
            file_paths.append({"filename": filename, "url": f"/static/files/{filename}"})
        else:
            file_paths.append({"filename": filename, "error": "File not found"})
    return JSONResponse(file_paths)

@app.post('/api/submit-objective')
def submit_objective(selected_objective:str):
    try: 


@app.get("/")
def read_root():
    return {"message": "Welcome to the File Upload API"}
