from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
    path('contact/', views.contact, name='contact'),
    path('careers/', views.careers, name='careers'),
path('admin-login/', views.admin_login, name='admin_login'),
path('admin-logout/', views.admin_logout, name='admin_logout'),
path('dashboard/', views.dashboard, name='dashboard'),
path('dashboard/leads/', views.dashboard_leads, name='dashboard_leads'),
path('dashboard/jobs/', views.dashboard_jobs, name='dashboard_jobs'),
path('dashboard/job-openings/', views.dashboard_job_openings, name='dashboard_job_openings'),
path('dashboard/job-openings/add/', views.add_job_opening, name='add_job_opening'),
path('dashboard/job-openings/edit/<int:id>/', views.edit_job_opening, name='edit_job_opening'),
path('dashboard/job-openings/delete/<int:id>/', views.delete_job_opening, name='delete_job_opening'),

]