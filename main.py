from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from typing import List
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import io

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Project": "Carbon footprint estimator"}


@app.get("/companies/", response_model=List[schemas.Company])
def read_companies(sort_by: str = "write energy_usage or waste_generation or business_travel or total", db: Session = Depends(get_db)):
    companies = crud.get_companies(db, sort_by=sort_by)
    return companies

@app.get("/generate_report/", response_model=List[schemas.Company])
def generate_report(sort_by: str = "", db: Session = Depends(get_db)):
    companies = crud.get_companies(db, sort_by=sort_by)
    if not companies:
        raise HTTPException(status_code=400, detail="No companies provided")
    
    response = generate_pdf_from_companies(companies,"report_sorted_"+sort_by)
    return Response(content=response, media_type="application/pdf")

# company_id will be used later
@app.post(
    "/companies/",
    response_model=schemas.Company,
    responses={
        # example of succss response
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {
                        "id":1,
                        "title": "My Company",
                        "electricity": 5000,
                        "natural_gas": 10000,
                        "fuel": 15000,
                        "waste": 10000,
                        "recycled_percent": 0.3,
                        "business_travels": 1000000,
                        "fuel_efficency": 80,
                        "company_id": 1,
                        "energy_usage": 417693.6,
                        "waste_generation": 32399.999999999996,
                        "business_travel": 28875.0,
                        "total": 478968.6,
                    }
                }
            },
        }
    },
)
async def create_company(
    company: Annotated[
        schemas.Company,
        Body(
            # input example
            examples=[
                {
                    "title": "MY company",
                    "electricity": 5000,
                    "natural_gas": 10000,
                    "fuel": 15000,
                    "waste": 10000,
                    "recycled_percent": 0.3,
                    "business_travels": 1000000,
                    "fuel_efficency": 80,
                }
            ],
        ),
    ],
    db: Session = Depends(get_db),
):

   return crud.create_company(db=db, company=company)

def generate_pdf_from_companies(companies: list[schemas.Company],file_name):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set up PDF content
    data = [['Company ID', 'Title','energy_usage','waste_generation','business_travel','total',"Measurments"]]  # Table header
    for company in companies:
        data.append([company.id, str(company.title),company.energy_usage,company.waste_generation,company.business_travel,company.total, "KG Co2"])

    # Create table
    table = Table(data)

    # Add style to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Determine the position of the table
    table_width, table_height = table.wrap(400, 200)
    x = (pdf._pagesize[0] - table_width) / 2  # Center the table horizontally
    y = 550  # Adjust this value to move the table down

    # Draw table on the PDF
    table.drawOn(pdf, x, y)

    pdf.save()

    # Save PDF to a file
    with open("reports/"+file_name+".pdf", 'wb') as file:
        file.write(buffer.getvalue())
        
    buffer.seek(0)
    return buffer.read()