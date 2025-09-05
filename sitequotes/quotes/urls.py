from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='home'),
	path('top-10', views.top, name='top')
]