from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, Ban
from .serializers import BanSerializer, BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True, methods=['post'])
    def ban(self, request, pk=None):
        book = self.get_object()
        serializer = BanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(book=book)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class BanViewSet(viewsets.ModelViewSet):
    queryset = Ban.objects.all()
    serializer_class = BanSerializer

