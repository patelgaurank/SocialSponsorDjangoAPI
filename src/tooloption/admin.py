from django.contrib import admin
from .models import DomElement
# Register your models here.DomElement

@admin.register(DomElement)
class DomElementAdmin(admin.ModelAdmin):
    list_display = ['DomElement_Id', 'section', 'subsection',]
    list_filter = ['created_at','section', 'subsection']
