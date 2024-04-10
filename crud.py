from sqlalchemy.orm import Session

import models, schemas


def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()


def create_company(db: Session, company: schemas.Company):
    db_company = models.Company(
        title=company.title,
        electricity=company.electricity,
        natural_gas=company.natural_gas,
        fuel=company.fuel,
        waste=company.waste,
        recycled_percent=company.recycled_percent,
        business_travels=company.business_travels,
        fuel_efficency=company.fuel_efficency,
        energy_usage=company.calculate_energy_usage(),
        waste_generation=company.calculate_waste_generation(),
        business_travel=company.calculate_business_travel(),
        total=company.calculate_total()
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company
