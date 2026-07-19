from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import LegalDocument

class LegalIndexView(ListView):
    model = LegalDocument
    template_name = 'legal/index.html'
    context_object_name = 'documents'

class LegalDocumentView(DetailView):
    model = LegalDocument
    template_name = 'legal/document.html'
    slug_field = 'slug'