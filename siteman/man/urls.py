from django.urls import path, re_path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [

    path('', views.ManHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>', views.ShowPost.as_view(), name='post'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),
    path('login/', views.login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:cat_slug>/', views.ManCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.ManTag.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page')
]
