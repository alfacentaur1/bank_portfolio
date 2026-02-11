from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_alt'),
    path('apps/', views.app_list, name='app_list'),
    path('apps/<int:app_id>/', views.app_detail, name='app_detail'),
    path('analysis/', views.global_analysis, name='analysis'),
    path('qa/', views.qa_view, name='qa'), 
    path('qa-chat/', views.qa_view, name='qa_view'), 
    path('mermaid/<int:app_id>/', views.generate_mermaid_view, name='generate_mermaid'),
    path('integrations/', views.integration_list, name='integration_list'),
    path('integrations/create/', views.integration_create, name='integration_create'),
    path('integrations/delete/<int:pk>/', views.integration_delete, name='integration_delete'),
]