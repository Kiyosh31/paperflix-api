from django.urls import path
from .views import *


urlpatterns = [
    path('admin-create/', admin_create, name='admin-create'),
    path('admin-login/', admin_login, name='admin-login'),
    path('admin-logout/<int:id_user>/', admin_logout, name='admin-logout'),
    path('admin-list/', admin_list, name='admin-list'),
    path('admin-update/<int:id_user>/', admin_update, name='admin-update'),

    path('user-list/', user_list, name='user-list'),
    path('user-detail/<int:id_user>/', user_detail, name='user-detail'),
    path('user-login/', user_login, name='user-login'),
    path('user-create/', user_create, name='user-create'),
    path('user-update/<int:id_user>/', user_update, name='user-update'),
    path('user-delete/<int:id_user>/', user_delete, name='user-delete'),
    path('user-activate/', user_activate, name='user-activate'),
    path('user-logout/<int:id_user>/', user_logout, name='user-logout'),
    path('user-cookies/', user_cookies, name='user-cookies'),

    path('papersuser-create/', papersuser_create, name='papersuser-create'),
    path('papersuser-list/', papersuser_list, name='papersuser-list'),
    path('papersuser-detail/<int:id_user>/<int:id_paper>/', papersuser_detail, name='papersuser-detail'),
    path('papersuser-update/<int:id_user>/<int:id_paper>/', papersuser_update, name='papersuser-update'),
    path('papersuser-delete/<int:id_papersuser>/', papersuser_delete, name='papersuser-delete'),
    
    path('paper-multiple-create/', paper_multiple_create, name='papers-multiple-create'),
    path('paper-create/', paper_create, name='papers-create'),
    path('paper-list/', paper_list, name='papers-list'),
    path('paper-latest/', paper_latest, name='papers-latest'),
    path('paper-random/', paper_random, name='papers-random'),
    path('paper-detail/<int:id_paper>/', paper_detail, name='papers-detail'),
    path('paper-search/', paper_search, name='papers-search'),
    path('paper-update/<int:id_paper>/', paper_update, name='papers-update'),
    path('paper-delete/<int:id_paper>/', paper_delete, name='papers-delete'),
    # path('paper-pagination/<int:id_category>/<int:last_paper>/', paper_pagination, name='papers-pagination'),

    path('category-multiple-create/', category_multiple_create, name='categories-multiple-create'),
    path('category-create/', category_create, name='category-create'),
    path('category-list/', category_list, name='category-list'),
    path('category-search/', category_search, name='category-search'),
    path('category-detail/<int:id_category>/', category_detail, name='category-detail'),
    path('category-update/<int:id_category>/', category_update, name='category-update'),
    path('category-delete/<int:id_category>/', category_delete, name='category-delete'),
    path('category-activate/<int:id_category>/', category_activate, name='category-activate'),
]
