from django.shortcuts import get_object_or_404
from user_app.views import UserView, s, Response
from .serializers import *

# Create your views here.


class AllBooksView(UserView):
    def get(self, request):
        books = request.user.books.all()
        return Response(BookSerializer(books, many=True).data)

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        new_book = BookSerializer(data=data, partial=True)
        if new_book.is_valid():
            new_book.save()
            return Response(new_book.data, status=s.HTTP_201_CREATED)
        else:
            return Response(new_book.errors, status=s.HTTP_400_BAD_REQUEST)


class ABookView(UserView):
    def get_a_book(self, user, book_id):
        return get_object_or_404(user.books, id=book_id)

    def get(self, request, book_id):
        return Response(BookSerializer(self.get_a_book(request.user, book_id)).data)

    def put(self, request, book_id):
        book = self.get_a_book(request.user, book_id)
        updated_book = BookSerializer(book, data=request.data, partial=True)
        if updated_book.is_valid():
            updated_book.save()
            return Response(updated_book.data)
        else:
            return Response(updated_book.errors, status=s.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id):
        book = self.get_a_book(request.user, book_id)
        book.delete()
        return Response("Book has been deleted")
