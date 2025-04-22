from pydantic import BaseModel, Field
from typing import List, Optional, Union

class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    years: Optional[str] = None

class Experience(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    start_date: Optional[str] = None  
    end_date: Optional[str] = None    
    duration: Optional[str] = None    
    description: Optional[str] = None 

class Project(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[List[str]] = Field(default_factory=list)

class Certification(BaseModel):
    name: Optional[str] = None
    year: Optional[str] = None

class ExtractionResponse(BaseModel):
    name: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    skills: List[str] = Field(default_factory=list)

    education: List[Union[str, Education]] = Field(default_factory=list)
    experience: List[Union[str, Experience]] = Field(default_factory=list)
    projects: List[Union[str, Project]] = Field(default_factory=list)
    certifications: List[Union[str, Certification]] = Field(default_factory=list)

    summary: Optional[str] = ""