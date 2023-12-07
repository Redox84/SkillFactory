from django.urls import path
from .views import *
from . import views

app_name = 'bulletin'

urlpatterns = [
    path('news/', NewsList.as_view(), name='news'),  # URL-шаблон для списка объявлений
    path('news/<int:pk>/', Detail.as_view(), name='detail'),  # URL-шаблон для полного объявления
    path('news/create/', views.Create.as_view(), name='create'),  # URL-шаблон для создания
    path('news/<int:pk>/edit/', Edit.as_view(), name='edit'),  # URL-шаблон для редактирования
    path('news/<int:pk>/delete/', Delete.as_view(), name='delete'),  # URL-шаблон для удаления
    path('news/<int:pk>/respon/create/', views.ResponCreate.as_view(), name='respon_create'),  # URL-шаблон отклика

    path('respon/<int:pk>/', ResponDetail.as_view(), name='respon_d'),
    path('respon/<int:pk>/delete/', ResponDelete.as_view(), name='respon_del'),
    path('respon/<int:pk>/respon_accept/', views.respon_accept, name='respon_accept'),
    path('prodected_page/', ProtectedView.as_view(), name='lk'),  # URL-шаблон страницы личного кабинета
    path('category/<int:pk>/', CategoryView.as_view(), name='category'),  # URL-шаблон списка категорий


]