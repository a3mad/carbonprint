from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException
from typing import List
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = crud.get_companies(db, skip=skip, limit=limit)
    return companies

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
