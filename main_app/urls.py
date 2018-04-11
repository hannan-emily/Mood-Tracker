from django.urls import path, include
from django.conf.urls.static import static
from . import views


urlpatterns = [
	path('', views.index, name='index'),
	path('<int:cat_id>/', views.show, name='show'),
	path('post_url/', views.post_cat, name='post_cat'),
	path('user/<username>/', views.profile, name='profile'),
	path('login/', views.login_view, name="login"),
	path('logout/', views.logout_view, name="logout"),
	path('signup/', views.signup, name='signup'),
	path('like_cat/', views.like_cat, name='like_cat'),
	path('<int:cat_id>/edit/', views.edit_cat, name='edit_cat'),
	path('<int:cat_id>/destroy/', views.delete_cat, name="delete_cat"),
	path('<int:cat_id>/toy/create/', views.create_toy, name='create_toy'),
	path('toy/<int:toy_id>/', views.show_toy, name='show_toy'),
	path('api/', views.api, name='api'),
	path('motion_result/', views.motion_result, name='motion_result'),
	path('history/', views.history, name='history'),
	path('chart/', views.chart, name='chart'),
	path('gallery/', views.gallery, name='gallery'),
	path('sample/', views.sample, name='sample'),
]
