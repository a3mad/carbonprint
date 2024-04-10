from pydantic import BaseModel, Field

class Company(BaseModel):
    #fields' type, validations, title, and description
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
    energy_usage: str = None
    waste_generation: str = None
    business_travel: str = None
    total: str = None