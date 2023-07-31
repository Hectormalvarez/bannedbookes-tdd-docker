from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

from .models import Book, Ban
from .serializers import BanSerializer, BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        # Get the nested books data from the request data
        books_data = request.data

        # List to store the created book IDs
        created_book_ids = []

        for book_data in books_data:
            # Get the nested bans data for this book
            bans_data = book_data.pop("bans", [])

            serializer = self.get_serializer(data=book_data)
            if serializer.is_valid():
                self.perform_create(serializer)
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Create nested bans after creating the book instance
            book_id = serializer.instance.id
            created_book_ids.append(book_id)

            for ban_data in bans_data:
                ban_data["book"] = book_id

            ban_serializer = BanSerializer(data=bans_data, many=True)
            if ban_serializer.is_valid():
                ban_serializer.save()
            else:
                print(ban_serializer.errors)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class BanViewSet(viewsets.ModelViewSet):
    queryset = Ban.objects.all()
    serializer_class = BanSerializer
