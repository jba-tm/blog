from django.urls import path
from .views import ContentDetailPrintView


urlpatterns = [
    path('<str:slug>/pdf', ContentDetailPrintView.as_view(), name='content-pdf'),
]
