from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [
    path(r'categories/', views.get_data, name='get_data'),
    path(r'categories/submit_data/', views.submit_data, name='submit_data'),
    path(r'categories/<int:pk>/', views.category_detail, name='category_tree'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)