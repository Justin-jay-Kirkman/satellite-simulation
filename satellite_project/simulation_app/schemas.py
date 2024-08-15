from ninja import ModelSchema, Schema
from .models import Spacecraft, Company
from ninja.orm import create_schema

CompanySchema = create_schema(Company, depth=1, name='Company')
CompanyCreateSchema = create_schema(Company, fields=['name'], name='Company Create')
SpacecraftSchema = create_schema(Spacecraft, name='Spacecraft')
SpacecraftCreateSchema = create_schema(Spacecraft, fields=['name', 'status'], name='Spacecraft Create')
SpacecraftStatusSchema = create_schema(Spacecraft, fields=['status'], name='Spacecraft Status')

class CompanySpacecraftAdd(Schema):
    spacecraft_slug: str


class Error(Schema):
    message: str
