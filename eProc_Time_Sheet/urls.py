from django.urls import path

from . import views
from .views.time_sheet_views import  get_project_details

app_name = 'eProc_Time_Sheet'

# Defining the mapping between URLs and views
urlpatterns = [
    path('get_project_details/', get_project_details, name='get_project_details'),
    # path('project_efforts/', project_efforts, name='project_efforts'),
]
