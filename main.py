import os
import datetime
import uuid
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import StreamingResponse
import io
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from docxtpl import DocxTemplate
from model import InputData
from utils.dropdown_service import DISTRICTS, BANKS
from utils.translate_text import to_marathi
from PyPDF2 import PdfMerger

TEMPLATE_DOC = "templates/DAJGUA_Form.docx"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def format_date(dt: str) -> str:
    dt = datetime.datetime.strptime(dt, "%Y-%m-%d")
    return dt.strftime("%d/%m/%Y")


UPLOAD_DIR = "uploads"
MERGED_DIR = "merged"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MERGED_DIR, exist_ok=True)

@app.get("/pdf-merger", response_class=HTMLResponse)
def upload_form(request: Request):
    """UI for uploading PDFs."""
    return templates.TemplateResponse(
        "pdf_merger.html",
        {
            "request": request
        }
    )


@app.post("/merge-pdfs")
async def merge_pdfs(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No PDF files uploaded")

    merger = PdfMerger()

    try:
        # Merge PDFs in memory
        for pdf in files:
            if pdf.content_type != "application/pdf":
                raise HTTPException(status_code=400, detail=f"{pdf.filename} is not a valid PDF")

            pdf_bytes = await pdf.read()
            merger.append(io.BytesIO(pdf_bytes))

        # Output PDF stored in memory
        output_buffer = io.BytesIO()
        merger.write(output_buffer)
        merger.close()

        output_buffer.seek(0)

        # Dynamic filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"merged_{timestamp}.pdf"

        return StreamingResponse(
            output_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF merge failed: {str(e)}")


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
            if "_marathi" not in key:
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

@app.post("/translate")
async def translate_text(payload: dict):
    text = payload.get("text", "")
    marathi = to_marathi(text)
    return {"marathi": marathi}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)