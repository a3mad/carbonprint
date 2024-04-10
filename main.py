from typing import Annotated

from fastapi import Body, FastAPI
from schemas import Company

app = FastAPI()


@app.get("/")
def read_root():
    return {"Project": "Carbon footprint estimator"}


# company_id will be used later
@app.put(
    "/companies/{company_id}",
    response_model=Company,
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
async def update_company(
    company_id: int,
    company: Annotated[
        Company,
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
    energy_usage = (
        (company.electricity * 12 * 0.0005)
        + (company.natural_gas * 12 * 0.0053)
        + (company.fuel * 12 * 2.32)
    )
    waste_generation = company.waste * 12 * (0.57 - company.recycled_percent)
    business_travel = company.business_travels * (1 / company.fuel_efficency) * 2.31
    result = {
        "company_id": company_id,
        "electricity": company.electricity,
        "natural_gas": company.natural_gas,
        "fuel": company.fuel,
        "waste": company.waste,
        "recycled_percent": company.recycled_percent,
        "business_travels": company.business_travels,
        "fuel_efficency": company.fuel_efficency,
        "energy_usage": str(energy_usage) + " " + "KG Co2/year",
        "waste_generation": str(waste_generation) + " " + "KG Co2/year",
        "business_travel": str(business_travel) + " " + "KG Co2/year",
        "total": str(energy_usage + waste_generation + business_travel)
        + " "
        + "KG Co2/year",
    }
    return result
