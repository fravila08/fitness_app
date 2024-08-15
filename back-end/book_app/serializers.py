from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class ReadingSummarySerializer(ModelSerializer):
    class Meta:
        model = ReadingSummary
        fields = "__all__"


class BookSerializer(ModelSerializer):
    reading_summaries = ReadingSummarySerializer(many=True)

    class Meta:
        model = Book
        fields = "__all__"
