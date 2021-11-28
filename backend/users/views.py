from django.shortcuts import get_object_or_404
from rest_framework import filters,  viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import (UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
    )
    def me(self, request):
        if request.method == "GET":
            user = get_object_or_404(User, username=request.user.username)
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)
        headers = self.get_success_headers(serializer.validated_data)
        return Response(serializer.validated_data, headers=headers)
