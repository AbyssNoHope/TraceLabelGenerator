from django.urls import path
import backend.views as views

urlpatterns = [
    path('add_books/', views.add_book),
    path('show_books/', views.show_books),
]