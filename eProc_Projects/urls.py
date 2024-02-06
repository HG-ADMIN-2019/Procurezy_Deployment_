from django.urls import path

from eProc_Users.views import register_page
from . import views
from .views.project import time_sheet, proj_user_search, proj_register_page, generate_guid, save_project_db, \
    delete_project, project_config

app_name = 'eProc_Projects'

# Defining the mapping between URLs and views
urlpatterns = [
    path('time_sheet/', time_sheet, name='time_sheet'),
    path('proj_user_search/', proj_user_search, name='proj_user_search'),
    path('proj_register_user/', proj_register_page, name='register_page'),
    path('save_project_db', save_project_db, name='save_project_db'),
    path('generate_guid', generate_guid, name='generate_guid'),
    path('delete_project/', delete_project, name='delete_project'),
    path('project_config/', project_config, name='project_config'),
]