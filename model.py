from pydantic import BaseModel, Field
from typing import Optional

class InputData(BaseModel):
    applicant_name: str = Field(..., description="The name of the applicant.")
    applicant_name_marathi: str = Field(None, description="The name of the applicant in Marathi.")
    applicant_address: str = Field(..., description="The address of the applicant.")
    applicant_address_marathi: str = Field(None, description="The address of the applicant in Marathi.")
    mobile_no: str = Field(..., description="The mobile number of the applicant.")
    age: Optional[int] = Field(None, description="The age of the applicant.")
    component: Optional[str] = Field(None, description="Component name")
    project_address: Optional[str] = Field(None, description="Project address")
    project_address_marathi: Optional[str] = Field(None, description="Project address in Marathi.")
    district: Optional[str] = Field(None, description="District")
    email: Optional[str] = Field(None, description="Email")
    aadhar_no: Optional[str] = Field(None, description="Aadhar")
    pancard: Optional[str] = Field(None, description="PAN")
    bank_name: Optional[str] = Field(None, description="Bank name")
    account_no: Optional[str] = Field(None, description="Account number")
    ifsc_code: Optional[str] = Field(None, description="IFSC code")
    profession: Optional[str] = Field(None, description="Profession")
    date: Optional[str] = Field(None, description="Date")
