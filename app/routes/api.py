from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from ..utils.extractor import extractTextAndSkills



router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        skills = extractTextAndSkills(file.filename, content)
        return {"skills": skills}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})