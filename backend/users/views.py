from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import LimitPageNumberPagination
from api.permissions import IsAdminOrReadOnly
from api.serializers import FollowSerializer
from users.models import Follow
from users.serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({
                'error': 'Нельзя подписываться на себя'
            }, status=status.HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(user=user, author=author).exists():
            return Response({
                'error': 'Вы уже подписаны на этого автора'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({
                'errors': 'Нельзя отписываться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Вы уже отписались'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(['get'], detail=False,
            permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        if not queryset.exists():
            return Response({'error': 'Вы еще ни на кого не подписаны'},
                            status=status.HTTP_400_BAD_REQUEST)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
