import os
import datetime
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
import io
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from docxtpl import DocxTemplate
from model import InputData
from utils.dropdown_service import DISTRICTS, BANKS
from utils.translate_text import to_marathi

TEMPLATE_DOC = "templates/DAJGUA_Form.docx"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def format_date(dt: str) -> str:
    dt = datetime.datetime.strptime(dt, "%Y-%m-%d")
    str_date = dt.strftime("%d/%m/%Y")
    return dt.strftime("%d/%m/%Y")


@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse(
        "form.html",
        {
            "request": request,
            "districts": DISTRICTS,
            "banks": BANKS
        },
    )


@app.post("/fill-docx")
async def fill_docx(payload: InputData, background_tasks: BackgroundTasks):
    print("Request Received: ", datetime.datetime.now())
    if not os.path.exists(TEMPLATE_DOC):
        raise HTTPException(500, "Template DOCX not found.")

    data_dict = payload.model_dump()
    context = {}

    # If user selected Other → override with manual bank name
    if data_dict.get("bank_name") == "Other":
        manual_name = data_dict.get("bank_name_other")
        if manual_name:
            data_dict["bank_name"] = manual_name

    fields_to_be_translated = [
        "applicant_name",
        "applicant_address",
        "district",
        "project_address"
    ]
    context["Aadhar_no"] = data_dict["aadhar_no"]
    for key, val in data_dict.items():
        val = "" if val is None else str(val)
        if key == "date":
            context[key] = format_date(val)
        else:
            context[key] = val
        context[f"{key}_english"] = val
        if key in fields_to_be_translated:
            context[f"{key}_marathi"] = to_marathi(val)
    print("Request Translated: ", datetime.datetime.now())
    doc = DocxTemplate(TEMPLATE_DOC)
    doc.render(context)
    print("Tags Replaced: ", datetime.datetime.now())
    output_stream = io.BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)

    # Dynamic filename based on applicant name
    filename = f"{data_dict['applicant_name'].replace(' ', '_')}_form.docx"

    return StreamingResponse(
        output_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)