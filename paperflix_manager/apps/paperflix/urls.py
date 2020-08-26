from django.urls import path
from .views import *


urlpatterns = [
    path('paper/', showb64file, name='paper'),

    path('user-list/', user_list, name='user-list'),
    path('user-detail/<int:id_user>/', user_detail, name='user-detail'),
    path('user-login/', user_login, name='user-login'),
    path('user-create/', user_create, name='user-create'),
    path('user-update/<int:id_user>/', user_update, name='user-update'),
    path('user-delete/<int:id_user>/', user_delete, name='user-delete'),
    path('user-activate/<int:id_user>/', user_activate, name='user-activate'),

    path('papersuser-create/', papersuser_create, name='papersuser-create'),
    path('papersuser-list/', papersuser_list, name='papersuser-list'),
    path('papersuser-detail/<int:id_user>/', papersuser_detail, name='papersuser-detail'),
    path('papersuser-update/<int:id_user>/', papersuser_update, name='papersuser-update'),

    path('paper-create/', paper_create, name='papers-create'),
    path('paper-list/', paper_list, name='papers-list'),
    path('paper-detail/<int:id_paper>/', paper_detail, name='papers-detail'),
    path('paper-update/<int:id_paper>/', paper_update, name='papers-update'),

    path('category-create/', category_create, name='category-create'),
    path('category-list/', category_list, name='category-list'),
    path('category-detail/<int:id_category>/', category_detail, name='category-detail'),
    path('category-update/<int:id_category>/', category_update, name='category-update'),
    path('category-delete/<int:id_category>/', category_delete, name='category-delete'),
    path('category-activate/<int:id_category>/', category_activate, name='category-activate'),

    path('categorypaper-create/', categorypaper_create, name='categorypaper-activate'),
    path('categorypaper-list/', categorypaper_list, name='categorypaper-list'),
    path('categorypaper-detail/<int:id_categorypaper>/', categorypaper_detail, name='categorypaper-detail'),
    path('categorypaper-update/<int:id_categorypaper>/', categorypaper_update, name='categorypaper-update'),
]
