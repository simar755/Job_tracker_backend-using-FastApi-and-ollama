# This can be a placeholder for now. You can extend this model for more detailed request payloads in the future.
from pydantic import BaseModel

class ExtractionRequest(BaseModel):
    file: bytes  # Can be expanded if needed
