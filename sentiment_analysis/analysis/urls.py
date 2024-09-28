from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register_user, name = 'register'),
    path('view/<int:record_id>/', views.view_chat, name='view_chat'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_chat/', views.add_chat, name = 'add_chat'),
    path('update/<int:pk>/', views.update_record, name='update_record'),


]
