from django.urls import path
from .views import *

urlpatterns = [
    path('', api_overview, name='api-overview'),
    path('user-list/', user_list, name='user-list'),
    path('user-detail/<int:id_user>/', user_detail, name='user-detail'),
    path('user-create/', user_create, name='user-create'),
    path('user-update/<int:id_user>/', user_update, name='user-update'),
    path('user-delete/<int:id_user>/', user_delete, name='user-delete'),
]
