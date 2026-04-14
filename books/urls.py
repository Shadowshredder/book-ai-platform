from django.urls import path
from .views import get_books, get_book_detail, add_book, get_summary
from .views import ask_question

urlpatterns = [
    path('books/', get_books),
    path('books/<int:id>/', get_book_detail),
    path('books/add/', add_book),
    path('books/<int:id>/summary/', get_summary), 
    path('books/<int:id>/ask/', ask_question),  # 👈 ADD THIS
]