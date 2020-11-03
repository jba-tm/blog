from django.urls import path
from .views import ApiUserRecordView

app_name = 'api'
urlpatterns = [
    path('user/', ApiUserRecordView.as_view(), name='users'),
]
