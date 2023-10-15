from django.urls import path
from core import views


urlpatterns = [
    path('issue/', views.IssueView.as_view()),
    path('issue/<int:pk>/', views.IssueDetail.as_view())
]