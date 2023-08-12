from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


from .pagination import LimitPageNumberPagination
from .permissions import IsAuthorPermissions
from recipes.models import (Tag, Recipe, Ingredient, Favorite,
                            ShoppingCart,)
from users.models import Follow, User
from .serializers import (TagSerializer, RecipeSerializer,
                          RecipeCreateSerializer, IngredientSerializer,
                          FavoriteSerializer, FollowSerializer,
                          FollowersSerializer, ShoppingCartSerializer,
                          )
from .filters import RecipeFilter, IngredientFilter


class TagViewSet(ModelViewSet):
    """Вьюсет для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    """Вьюсет для рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, ]
    pagination_class = LimitPageNumberPagination
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorPermissions, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(ModelViewSet):
    """Вьюсет для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    permission_classes = [AllowAny, ]


class FavoriteViewSet(ModelViewSet):
    """Вьюсет для добавление в избранное."""
    permission_classes = [IsAuthenticated, ]
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class Follows(generics.RetrieveDestroyAPIView,
              generics.ListCreateAPIView):
    """Вьюсет для подписки или отписки."""
    permission_classes = [IsAuthenticated, ]
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        '''Создание подписки.'''
        user_author = get_object_or_404(User, id=self.kwargs['user_id'])
        subscribe = request.user.follower.create(author=user_author)
        serializer = self.get_serializer(subscribe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, author_id):
        user = request.user
        author = get_object_or_404(User, id=author_id)
        obj = get_object_or_404(Follow, user=user, author=author)
        obj.delete()


class FollowersViewSet(ModelViewSet):
    """Вьюсет для отображения подписчиков."""
    queryset = User.objects.all()
    serializer_class = FollowersSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        queryset = User.objects.filter(author__user=user)
        page = self.paginate_queryset(queryset)
        context = {'request': request}
        serializer = FollowersSerializer(
            page, many=True, context=context
        )
        return self.get_paginated_response(serializer.data)


class ShoppingCartViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'recipe': id
        }
        recipe = get_object_or_404(Recipe, id=id)
        if not ShoppingCart.objects.filter(
           user=request.user, recipe=recipe).exists():
            context = {'request': request}
            serializer = ShoppingCartSerializer(
                data=data, context=context)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        if ShoppingCart.objects.filter(
           user=request.user, recipe=recipe).exists():
            ShoppingCart.objects.filter(
                user=request.user, recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
