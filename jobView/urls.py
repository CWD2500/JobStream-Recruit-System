from django.urls import path
from . import views


urlpatterns = [
    # path ...
    path('' , views.home , name="home"),
    path('about/' , views.about , name="about"),
    path('show/list/job/<slug:slug>/', views.job_list, name='job-list'),
    path('show/list/job/details/<slug:slug>/' , views.apply_for_job_details  , name='job-details'),
 
    path('update-application-status/<int:application_id>/<str:status>/', views.update_application_status, name='update-application-status'),
    path('mark_all_notifications_read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),


    # Searching 
        path('search/', views.job_search, name='job-search'), 
]
