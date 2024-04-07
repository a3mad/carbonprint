from typing import Annotated

from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


app = FastAPI()


@app.get("/")
def read_root():
    return {"Project": "Carbon footprint estimator"}


class Company(BaseModel):
    electricity: float = Field(
        gt=0,
        title="Monthly electricity bill in EUR",
        description="What is your average monthly electricity bill in Euros?",
    )
    natural_gas: float = Field(
        gt=0,
        title="Monthly natural gas bill in EUR",
        description="What is your average monthly natural gas bill in Euros?",
    )
    fuel: float = Field(
        gt=0,
        title="Monthly fuel bill in EUR",
        description="What is your average monthly fuel bill in Euros?",
    )
    waste: float = Field(
        gt=0,
        title="Monthly waste generation in KG",
        description="How much waste do you generate per month in kilograms ?",
    )
    recycled_percent: float = Field(
        gt=0,
        title="Waste Recycling/composting percentage",
        description="How much of that generated waste is recycled or composted(in percentage)?",
    )
    business_travels: float = Field(
        gt=0,
        title="Total kilometer travelled per year for business prposes",
        description="How many kilometers do your employees travel per year for business purposes?",
    )
    fuel_efficency: float = Field(
        gt=0,
        title="Fuel efficency in L/100KM",
        description="What is the average fuel efficeny of the vichels used for business travel in liters per 100 kilometers?",
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "electricity": 5000,
                    "natural_gas": 1000,
                    "fuel": 15000,
                    "waste": 10000,
                    "recycled_percent": 0.3,
                    "business_travels": 1000000,
                    "fuel_efficency": 80,
                }
            ]
        }
    }


# class required for output format
class CarbonFootPrints(BaseModel):
    company_id: int
    energy_usage: str
    waste_generation: str
    business_travel: str
    total: str


# company_id will be used later
@app.put(
    "/companies/{company_id}",
    response_model=CarbonFootPrints,
    responses={
        # example of succss response
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {
                        "company_id": 1,
                        "energy_usage": "417693.6 KG Co2/year",
                        "waste_generation": "32399.999999999996 KG Co2/year",
                        "business_travel": "28875.0 KG Co2/year",
                        "total": "478968.6 KG Co2/year",
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
        Body(embed=True),
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
        "energy_usage": str(energy_usage) + " " + "KG Co2/year",
        "waste_generation": str(waste_generation) + " " + "KG Co2/year",
        "business_travel": str(business_travel) + " " + "KG Co2/year",
        "total": str(energy_usage + waste_generation + business_travel)
        + " "
        + "KG Co2/year",
    }
    return result
