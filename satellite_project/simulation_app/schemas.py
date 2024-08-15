from ninja import ModelSchema, Schema
from .models import Spacecraft, Company
from ninja.orm import create_schema

CompanyGetSchema = create_schema(Company, depth=1, name='Company')
CompanyCreateSchema = create_schema(Company, fields=['name'], name='Company Create')
SpacecraftGetSchema = create_schema(Spacecraft, name='Spacecraft')
SpacecraftCreateSchema = create_schema(Spacecraft, fields=['name', 'status'], name='Spacecraft Create')

