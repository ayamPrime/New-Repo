from django.contrib import admin
from .models import LegalDocument

@admin.register(LegalDocument)
class LegalDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
