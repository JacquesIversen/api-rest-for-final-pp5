from django.urls import path
from core import views


urlpatterns = [
    path('issue/', views.IssueView.as_view()),
    path('issue/<int:pk>/', views.IssueDetail.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('likes/', views.LikeList.as_view()),
    path('likes/<int:pk>/', views.LikeDetail.as_view()),
    path('dislikes/', views.DisLikeList.as_view()),
    path('dislikes/<int:pk>/', views.DisLikeDetail.as_view()),
]
