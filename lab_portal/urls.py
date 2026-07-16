from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_dashboard, name='home_dashboard'), # Homepage
    path('report/', views.report_issue, name='report_issue'), # Submit ticket form page
]
