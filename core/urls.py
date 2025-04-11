from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('coordinator_login/', views.coordinator_login, name='coordinator_login'),
    path('head_login/', views.head_login, name='head_login'),
    path('borehole/<str:pk>/', views.borehole_detail, name='borehole_detail'),
    path('orphans/', views.orphans, name='orphans'),
    path('feeding_projects/', views.feeding_projects, name='feeding_projects'),
    path('orphans_crud/', views.orphans_crud, name='orphans_crud'),
    #borehole detail
    path('dashboard/coordinator_boreholes/', views.coordinator_boreholes, name='coordinator_boreholes'),
    path('cooordinator_borehole_detail/<str:pk>/',views.coordinator_borehole_detail, name='cooordinator_borehole_detail'),
    
    # Dashboard URLs
    path('dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('dashboard/boreholes/', views.boreholes, name='boreholes'),
    path('dashboard/borehole/add/', views.add_borehole, name='add_borehole'),
    path('dashboard/borehole/update/<str:pk>/', views.update_borehole, name='update_borehole'),
    path('dashboard/borehole/delete/<str:pk>/', views.delete_borehole, name='delete_borehole'),
    path('dashboard/borehole/crud/', views.borehole_crud, name='borehole_crud'),
]