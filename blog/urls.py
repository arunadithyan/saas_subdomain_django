from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login1, name='login1'),
    path('home/',views.index,name='index'),
    path('create-tenant/', views.create_tenant, name='create_tenant'),
    path('success/', views.logout,name='logout'),
    path('register/',views.register, name='register'),
    path('articles', views.articles, name='articles'),
    path('<slug:article>/', views.article, name='article'),
    # path('login/', views.articles, name='articles'),
]