from ninja import NinjaAPI
from .models import Spacecraft, Company
from .schemas import SpacecraftGetSchema, CompanyCreateSchema, CompanyGetSchema, SpacecraftCreateSchema
from django.shortcuts import get_object_or_404
from ninja.security import django_auth

api = NinjaAPI(title="Satellite Simulation API", version="0.1")


@api.get("spacecrafts/", response=list[SpacecraftGetSchema], tags=["Spacecraft"])
def get_spacecrafts(request):
    return Spacecraft.objects.all()

@api.post("spacecrafts/", response={200: SpacecraftCreateSchema}, tags=["Spacecraft"])
def create_spacecraft(request, spacecraft: SpacecraftCreateSchema):
    spacecraft_data = spacecraft.model_dump()
    spacecraft_model = Spacecraft(**spacecraft_data)
    return spacecraft_model

@api.get("companies/{slug}", response=CompanyGetSchema, tags=["Company"])
def get_company(request, slug: str):
    company = get_object_or_404(Company, slug=slug)
    return company

@api.post("/companies/", response=CompanyCreateSchema, tags=["Company"])
def create_company(request, company: CompanyCreateSchema):
    company_data = company.model_dump()
    company_model = Company.objects.create(**company_data)
    return company_model
