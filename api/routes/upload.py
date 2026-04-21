from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
import shutil
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

@router.post("/file")
async def upload_files(files: list[UploadFile] = File(...)): # Change to List
    print(f"Received {len(files)} files") # Diagnostic line
    # uploaded_info = []
    uploaded_info = []

    for file in files:
        if file.content_type not in ALLOWED_TYPES:
            # We skip invalid files or you can raise an error
            continue

        filename = file.filename
        file_path = os.path.join(UPLOAD_DIR, filename)

        if os.path.exists(file_path):
            filename = f"{uuid.uuid4().hex[:8]}_{file.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)

        # Using the streaming method for safety
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        uploaded_info.append({"filename": filename, "at": file_path})

    if not uploaded_info:
        raise HTTPException(status_code=400, detail="No valid files were uploaded.")

    return {"message": f"Successfully uploaded {len(uploaded_info)} files", "files": uploaded_info}
