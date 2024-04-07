from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def read_root():
    return {"Project": "Carbon footprint estimator"}


class Company(BaseModel):
    monthly_electricity_bill_eur: float
    monthly_natural_gas_bill_eur: float
    monthly_fuel_bill_eur:float
    monthly_waste_generation_kg:float
    waste_recycled_percent:float
    yearly_business_travel_km:float
    avg_vechile_fuel_efficency_L100KM:float

# company_id will be used later
@app.put("/companies/{company_id}")
def update_company(item_id: int, company: Company):
    energy_usage=(company.monthly_electricity_bill_eur*12*0.0005)+(company.monthly_natural_gas_bill_eur*12*0.0053)+(company.monthly_fuel_bill_eur*12*2.32)
    waste_generation=company.monthly_waste_generation_kg*12*(0.57-company.waste_recycled_percent)
    business_travel=company.yearly_business_travel_km*(1/company.avg_vechile_fuel_efficency_L100KM)*2.31
    return {
        "carbon_footpring_yearly_KgCo2":{
        "energy_usage": str(energy_usage)+" "+"KG Co2/year",
        "waste_generation": str(waste_generation)+" "+"KG Co2/year",
        "business_travel": str(business_travel)+" "+"KG Co2/year",
        "total": str(energy_usage+waste_generation+business_travel)+" "+"KG Co2/year",
        }
        }
