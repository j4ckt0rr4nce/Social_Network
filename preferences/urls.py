from django.urls import path
from .views import MyPreferenceFormView


app_name = 'preferences'

urlpatterns = [
    path('add/', MyPreferenceFormView.as_view(), name='my-preferences-add-view'),
]