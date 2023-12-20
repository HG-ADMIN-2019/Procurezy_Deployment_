from django.urls import path
from . import views

app_name = 'eProc_Workflow'

# Defining the mapping between URLs and views
urlpatterns = [
    path('save_appr_status/', views.save_appr_status, name='save_appr_status'),
]
