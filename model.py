from fastapi import Form
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


    @classmethod
    def as_forn(
            cls,
            applicant_name: str = Form(...),
            applicant_name_marathi: str = Form(...),
            applicant_address: str = Form(...),
            applicant_address_marathi: str = Form(...),
            mobile_no: str = Form(...),
            age: Optional[int] = Form(None),
            component: Optional[str] = Form(None),
            project_address: Optional[str] = Form(None),
            project_address_marathi: Optional[str] = Form(None),
            district: Optional[str] = Form(None),
            email: Optional[str] = Form(None),
            aadhar_no: Optional[str] = Form(None),
            pancard: Optional[str] = Form(None),
            bank_name: Optional[str] = Form(None),
            account_no: Optional[str] = Form(None),
            ifsc_code: Optional[str] = Form(None),
            profession: Optional[str] = Form(None),
            date: Optional[str] = Form(None)
    ):
        return cls(
            applicant_name=applicant_name,
            applicant_name_marathi=applicant_name_marathi,
            applicant_address=applicant_address,
            applicant_address_marathi=applicant_address_marathi,
            mobile_no=mobile_no,
            age=age,
            component=component,
            project_address=project_address,
            project_address_marathi=project_address_marathi,
            district=district,
            email=email,
            aadhar_no=aadhar_no,
            pancard=pancard,
            bank_name=bank_name,
            account_no=account_no,
            ifsc_code=ifsc_code,
            profession=profession,
            date=date
        )
