from django.urls import path
from .views import ContentDetailPrintView
from .api import api_router

urlpatterns = [
    path('<str:slug>/pdf', ContentDetailPrintView.as_view(), name='content-pdf'),
    path('api/v2/', api_router.urls),
]
