from django.urls import path, include
from django.conf.urls.static import static
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('user/<username>/', views.profile, name='profile'),
	path('login/', views.login_view, name="login"),
	path('logout/', views.logout_view, name="logout"),
	path('signup/', views.signup, name='signup'),
	path('api/', views.api, name='api'),
	path('motion_result/', views.motion_result, name='motion_result'),
	path('history/', views.history, name='history'),
	path('chart/', views.chart, name='chart'),
	path('gallery/', views.gallery, name='gallery'),
	path('sample/', views.sample, name='sample'),
]
