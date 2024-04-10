from pydantic import BaseModel, Field

class Company(BaseModel):
    #fields' type, validations, title, and description
    id: int = None
    title: str = Field(
        min_length=1,
        max_length=50,
        title="Company title",
        description="what is your company name?",
    )
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
        le=1,
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
    energy_usage: float = None
    waste_generation: float = None
    business_travel: float = None
    total: float = None

    def calculate_energy_usage(self)->float:
         self.energy_usage=(self.electricity * 12 * 0.0005)+ (self.natural_gas * 12 * 0.0053)+ (self.fuel * 12 * 2.32)
         return self.energy_usage
    
    def calculate_waste_generation(self)->float:
        self.waste_generation = self.waste * 12 * (0.57 - self.recycled_percent)
        return self.waste_generation

    def calculate_business_travel(self)->float:
        self.business_travel = self.business_travels * (1 / self.fuel_efficency) * 2.31
        return self.business_travel

    def calculate_total(self)->float:
        self.total=self.energy_usage+self.waste_generation+self.business_travel
        return self.total

    class Config:
        #orm_mode = True
        from_attributes = True
       #underscore_attrs_are_private = True