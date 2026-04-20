from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid

router = APIRouter()

# Save uploaded files directly to the Gnosis app/data directory
# so the watchdog pipeline can detect and process them automatically
UPLOAD_DIR ="/code/app/data/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "application/pdf",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation"
}
'''
uncomment THIS WHILE DEPLOYING

import shutil
@router.post("/file")
def upload_file(file: UploadFile = File(...)): # Note: Removed 'async' since shutil is synchronous
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)

    if os.path.exists(file_path):
        filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

    # STREAM THE FILE INSTEAD OF LOADING TO RAM
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "File uploaded successfully", "filename": filename}

    '''
@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Keep the original filename for readability in the data directory
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)

    # If file already exists, prefix with UUID to avoid overwrite
    if os.path.exists(file_path):
        # filename = f"{uuid.uuid4().hex[:8]}_{file.filename} Will uncomment while implementing user based query retrival
        file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    print({"message": "File uploaded successfully", "filename": filename,"at":file_path})

    return {"message": "File uploaded successfully", "filename": filename,"at":file_path}
