from django.urls import path
from .views import LegalIndexView, LegalDocumentView

urlpatterns = [
    path('', LegalIndexView.as_view(), name='legal_index'),
    path('<slug:slug>/', LegalDocumentView.as_view(), name='legal_document'),
]