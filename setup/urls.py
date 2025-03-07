from django.contrib import admin
from django.urls import path, include
from .views import index  # Importando a view do index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('hangman/', include('hangman.urls')),
]
