from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Server
from .serializers import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling server-related operations.

    Attributes:
        queryset (QuerySet): The queryset containing all Server objects.
        serializer (ServerSerializer): The serializer class for Server objects.

    Methods:
        list(self, request): Handles the GET request to retrieve a list of servers based on query parameters.
        retrieve(self, request, pk): Handles the GET request to retrieve details of a specific server by its primary key.
    """

    queryset = Server.objects.all()
    serializer = ServerSerializer

    def list(self, request):
        """
        Handle GET request to retrieve a list of servers based on query parameters.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A response containing serialized server data.
        """
        category = request.query_params.get('category')
        qty = request.query_params.get('q')
        user = request.query_params.get('user') == "true"

        if category:
            self.queryset = self.queryset.filter(category=category)

        if user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if qty:
            self.queryset = self.queryset[:int(qty)]

        self.queryset = self.queryset.annotate(num_members=Count('member'))

        serializer = self.serializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Handle GET request to retrieve details of a specific server by its primary key.

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the server to retrieve.

        Returns:
            Response: A response containing serialized server data or a 404 error if not found.
        """
        server = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer(server)
        return Response(serializer.data)
