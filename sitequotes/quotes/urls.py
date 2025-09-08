from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('like/<int:pk>/', views.like_quote, name='like_quote'),
	path('dislike/<int:pk>/', views.dislike_quote, name='dislike_quote'),
	path('top/', views.top, name='top'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('add/', views.add_quote, name='add'),
]