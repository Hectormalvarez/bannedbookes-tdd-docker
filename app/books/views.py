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
        # Get the nested bans data from the request data
        bans_data = request.data.pop("bans", [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Create nested bans after creating the book instance
        for ban_data in bans_data:
            ban_data["book"] = serializer.instance.id
        ban_serializer = BanSerializer(data=bans_data, many=True)
        ban_serializer.is_valid(raise_exception=True)
        ban_serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    @action(detail=True, methods=["post"])
    def bans(self, request, pk=None):
        book = self.get_object()
        serializer = BanSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(book=book)
            return Response(serializer.data, status=201)
        print(serializer.errors)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=["get"])
    def search(self, request):
        title = request.GET.get("title", "")
        author = request.GET.get("author", "")

        # Filter the books based on the provided title and/or author
        # Using Q objects to perform OR operation between title and author filters
        books = Book.objects.filter(
            Q(title__icontains=title) | Q(author__icontains=author)
        )

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BanViewSet(viewsets.ModelViewSet):
    queryset = Ban.objects.all()
    serializer_class = BanSerializer
