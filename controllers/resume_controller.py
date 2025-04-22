from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.resume_parser_service import parse_resume
from models.extraction_response import ExtractionResponse
from safe_json_parser import parse_resume_json

# Define the router with a prefix '/resumes' and tag for documentation
router = APIRouter(prefix="/resumes", tags=["Resumes"])

# Define the endpoint for extracting resume details (POST method)
@router.post("/extract/")
async def extract_resume_info(file: UploadFile = File(...)):
    try:
        # Read the content of the uploaded file asynchronously
        file_content = await file.read()
        
        # Call the parse_resume function to extract details from the resume
        raw_extracted_output = parse_resume(file_content)

        # If the extracted output is a string (raw text), parse it into structured data
        if isinstance(raw_extracted_output, str):
            parsed_data = parse_resume_json(raw_extracted_output)
        else:
            # If the output is already in structured data (e.g., dictionary), use it directly
            parsed_data = raw_extracted_output

        # Return the parsed data as a JSON response using the ExtractionResponse model
        return JSONResponse(content=jsonable_encoder(ExtractionResponse(**parsed_data)))

    except Exception as e:
        # Handle any exceptions and return an HTTP 500 Internal Server Error
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
