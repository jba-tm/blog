from django.urls import path
from .views import ApiUserRecordView

app_name = 'api'
urlpatterns = [
    path('users/', ApiUserRecordView.as_view(), name='api_users'),
]
