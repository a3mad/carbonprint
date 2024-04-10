from typing import Annotated

from fastapi import Body, FastAPI, HTTPException
import schemas

app = FastAPI()


@app.get("/")
def read_root():
    return {"Project": "Carbon footprint estimator"}


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
):
   
    result = {
        "electricity": company.electricity,
        "natural_gas": company.natural_gas,
        "fuel": company.fuel,
        "waste": company.waste,
        "recycled_percent": company.recycled_percent,
        "business_travels": company.business_travels,
        "fuel_efficency": company.fuel_efficency,
        "energy_usage": str(company.calculate_energy_usage()) + " " + "KG Co2/year",
        "waste_generation": str(company.calculate_waste_generation()) + " " + "KG Co2/year",
        "business_travel": str(company.calculate_business_travel()) + " " + "KG Co2/year",
        "total": str(company.calculate_total())+" "+ "KG Co2/year",
    }
    return result
