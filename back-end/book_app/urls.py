from django.urls import path
from .views import *
from .summary_views import *

urlpatterns = [
    path(
        "", 
        AllBooksView.as_view(), 
        name="all books"
    ),
    path(
        "<int:book_id>/", 
        ABookView.as_view(), 
        name="a book"
    ),
    path(
        "<int:book_id>/summaries/", 
        AllSummariesView.as_view(), 
        name="all summaries"
    ),
    path(
        "<int:book_id>/summaries/<int:summary_id>/",
        ASummaryView.as_view(),
        name="a summary",
    ),
]
