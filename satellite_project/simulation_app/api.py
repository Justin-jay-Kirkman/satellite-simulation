from ninja import NinjaAPI
from .models import Spacecraft, Company, SPACECRAFT_STATUS
from .schemas import SpacecraftSchema, CompanyCreateSchema, CompanySchema, SpacecraftCreateSchema, Error, SpacecraftStatusSchema, CompanySpacecraftAdd
from django.shortcuts import get_object_or_404
from ninja.security import django_auth

api = NinjaAPI(title="Satellite Simulation API", version="0.1")


@api.get("/companies/", response=list[CompanySchema], tags=["Company"])
def get_all_companies(request):
    return Company.objects.all()


@api.get("companies/{company_slug}", response=CompanySchema, tags=["Company"])
def get_company(request, company_slug: str):
    company = get_object_or_404(Company, slug=company_slug)
    return company


@api.post("/companies/", response=CompanySchema, tags=["Company"])
def create_company(request, company: CompanyCreateSchema):
    company_data = company.model_dump()
    company_model = Company.objects.create(**company_data)
    return company_model


@api.post("/companies/{company_slug}/add-spacecraft", response={200: CompanySchema, 404: Error}, tags=["Company"])
def add_spacecraft(request, company_slug: str, spacecraft: CompanySpacecraftAdd):
    company = get_object_or_404(Company, slug=company_slug)
    if spacecraft.spacecraft_slug:
        spacecraft = get_object_or_404(Spacecraft, slug=spacecraft.spacecraft_slug)
        company.satellites.add(spacecraft)
        company.save()
    else:
        return 404, {'message': 'Spacecraft not found'}
    return company


@api.get("spacecrafts/", response=list[SpacecraftSchema], tags=["Spacecraft"])
def get_spacecrafts(request):
    return Spacecraft.objects.all()


@api.post("spacecrafts/", response={200: SpacecraftSchema, 422: Error}, tags=["Spacecraft"])
def create_spacecraft(request, spacecraft: SpacecraftCreateSchema):
    if spacecraft.status in SPACECRAFT_STATUS:
        spacecraft_data = spacecraft.model_dump()
        spacecraft_model = Spacecraft.objects.create(**spacecraft_data)
    else:
        return 422, {'message': 'Spacecraft status is not valid'}
    return spacecraft_model


@api.put("spacecrafts/{spacecraft_slug}/update-status", response={200: SpacecraftSchema, 404: Error, 422: Error}, tags=["Spacecraft"])
def update_spacecraft(request, spacecraft_slug: str, spacecraft: SpacecraftStatusSchema):
    if spacecraft.status not in SPACECRAFT_STATUS:
        return 422, {'message': 'Spacecraft status is not valid'}
    spacecraft_model = get_object_or_404(Spacecraft, slug=spacecraft_slug)
    spacecraft_model.status = spacecraft.status
    spacecraft_model.save()
    return spacecraft_model







