from django.urls  import path
from . import views

urlpatterns = [
    # path ...

    path('register', views.register_job_seeker, name='register'),
    path('check-email/', views.check_email, name='check_email'),
    path('register/profile/data/user/' , views.datauser , name='data-users'),
    path('profile/user/<slug:slug>/' , views.profileUser , name='profile-users'),
    path('register/profile/user/edit/<str:slug>/' , views.editUserProfile , name='profile-users-edit'),
    path('register/profile/user/delete/<str:id>/' , views.delete_data_profile , name='profile-users-delete'),

    
    path('profile/orders/', views.profile_order, name='orders'),
    path('profile/orders/delete/<int:id>', views.order_delete, name='orders-delete'),
    # path('register/profile/user/edit/<int:id>/' , views.edit_data_profile , name='profile-users-edit-data'),

    path('register/employer/', views.register_employer, name='register-employer'),
    
    path('profile/employer/add/job/<str:slug>/', views.addJob, name='employer-addJob'),
    path('profile/employer/edit/job/<str:slug>/', views.edit_job_employer, name='employer-job-edit'),
    path('profile/employer/edit/employer/<str:slug>/', views.edit_employer_data, name='employer-edit'),
    # path('ajax/register-employer/', views.ajax_register_employer, name='ajax_register_employer'),
   
   
    path('login/', views.logins, name='logins'),
    path('logout/', views.logouts, name='logout'),


    path('reset-password/', views.reset_password, name='reset_password'),




]
