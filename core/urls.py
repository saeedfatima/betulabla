from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('logout', views.user_logout, name='user_logout'),
    path('dashboard/coordinator_login/', views.coordinator_login, name='coordinator_login'),
    path('dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('head_login/', views.head_login, name='head_login'),
    path('borehole/<str:pk>/', views.borehole_detail, name='borehole_detail'),
    path('core/orphans/', views.orphans, name='orphans'),
    path('orphans_detail/<str:pk>/', views.orphans_detail, name='orphans_detail'),
    path('delete_orphan/<str:pk>/', views.delete_orphan, name='delete_orphan'),
    path('update_orphan/<str:pk>/', views.update_orphan, name='update_orphan'),
    path('add_orphans/', views.add_orphan, name='add_orphan'),
    path('feeding_projects/', views.feeding_projects, name='feeding_projects'),
    path('orphans_crud/', views.orphans_crud, name='orphans_crud'),
    #borehole detail
    path('core/boreholes/', views.boreholes, name='boreholes'),
    path('borehole_detail/<str:pk>/',views.borehole_detail, name='borehole_detail'),
    
    # Dashboard URLs
    path('dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('dashboard/borehole/add/', views.add_borehole, name='add_borehole'),
    path('dashboard/borehole/update/<str:pk>/', views.update_borehole, name='update_borehole'),
    path('dashboard/borehole/delete/<str:pk>/', views.delete_borehole, name='delete_borehole'),
    path('borehole_crud/', views.borehole_crud, name='borehole_crud'),
    
    #static pages
    path('feeding_projects/', views.feeding_projects, name='feeding_projects'),
    path('feeding_project_detail/<str:pk>/', views.feeding_project_detail, name='feeding_project_detail' ),
    #feeding project crud
    path('feeding_projects_crud/', views.feeding_projects_crud, name='feeding_projects_crud'),
    path('add_feeding_project/', views.add_feeding_project, name='add_feeding_project'),
    path('update_feeding_project/<str:pk>/', views.update_feeding_project, name='update_feeding_project'),
    path('delete_feeding_project/<str:pk>/', views.delete_feeding_project, name='delete_feeding_project'),

]