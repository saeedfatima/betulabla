from django.urls import path
from . import views

urlpatterns = [
    # Static pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    
    path('contact/', views.contact, name='contact'),

    # Authentication
    path('login/', views.loginUser, name='login'),
    path('register/', views.RegisterUser, name="register"),
    path('logout/', views.user_logout, name='user_logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Orphans
    path('orphans/', views.orphans, name='orphans'),
    path('orphans/detail/<str:pk>/', views.orphans_detail, name='orphans_detail'),
    path('orphans/delete/<str:pk>/', views.delete_orphan, name='delete_orphan'),
    path('orphans/update/<str:pk>/', views.update_orphan, name='update_orphan'),
    path('orphans/add/', views.add_orphan, name='add_orphan'),
    path('orphans/crud/', views.orphans_crud, name='orphans_crud'),

    # Boreholes
    path('boreholes/', views.boreholes, name='boreholes'),
    path('boreholes/detail/<str:pk>/', views.borehole_detail, name='borehole_detail'),
    path('boreholes/add/', views.add_borehole, name='add_borehole'),
    path('boreholes/update/<str:pk>/', views.update_borehole, name='update_borehole'),
    path('boreholes/delete/<str:pk>/', views.delete_borehole, name='delete_borehole'),
    path('boreholes/crud/', views.borehole_crud, name='borehole_crud'),

    # Feeding Projects
    path('feeding-projects/', views.feeding_projects, name='feeding_projects'),
    path('feeding-projects/detail/<str:pk>/', views.feeding_project_detail, name='feeding_project_detail'),
    path('feeding-projects/add/', views.add_feeding_project, name='add_feeding_project'),
    path('feeding-projects/update/<str:pk>/', views.update_feeding_project, name='update_feeding_project'),
    path('feeding-projects/delete/<str:pk>/', views.delete_feeding_project, name='delete_feeding_project'),
    path('feeding-projects/crud/', views.feeding_projects_crud, name='feeding_projects_crud'),

    # Profile
    path('profile/', views.userprofile, name='userprofile'),
    path('dashboardprofile/edit/', views.editUserProfile, name='editUserProfile'),
]
