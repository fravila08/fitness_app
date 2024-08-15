from django.shortcuts import get_object_or_404
from django.utils import timezone
from user_app.views import UserView, s, Response
from .serializers import *


class AllSummariesView(UserView):
    def get(self, request, book_id):
        summaries = request.user.books.get(id=book_id).reading_summaries.all()
        return Response(ReadingSummarySerializer(summaries, many=True).data)

    def post(self, request, book_id):
        book = request.user.book.get(id=book_id)
        data = request.data.copy()
        data["book"] = book.id
        new_summary = ReadingSummarySerializer(data=data, partial=True)
        if new_summary.is_valid():
            book.last_read = timezone.now()
            book.current_page += new_summary.data.get("pages_read")
            book.save()
            new_summary.save()
            return Response(new_summary.data, status=s.HTTP_201_CREATED)
        else:
            return Response(new_summary.errors, status=s.HTTP_400_BAD_REQUEST)


class ASummaryView(UserView):
    def get_a_summary(self, obj, id):
        return get_object_or_404(obj, id=id)

    def get(self, request, book_id, summary_id):
        summary = self.get_a_summary(
            request.user.books.get(id=book_id).summaries, summary_id
        )
        return Response(ReadingSummarySerializer(summary).data)

    def put(self, request, book_id, summary_id):
        summary = self.get_a_summary(
            request.user.books.get(id=book_id).summaries, summary_id
        )
        updated_summary = ReadingSummarySerializer(
            summary, data=request.data, partial=True
        )
        if updated_summary.is_valid():
            updated_summary.save()
            return Response(updated_summary.data)
        else:
            return Response(updated_summary.errors, status=s.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id, summary_id):
        summary = self.get_a_summary(
            request.user.books.get(id=book_id).summaries, summary_id
        )
        summary.delete()
        return Response("A Summary has been deleted")
