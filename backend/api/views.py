from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.http import HttpResponse
from django.db.models import Sum

from .permissions import IsAuthorPermissions
from recipes.models import (Tag, Recipe, Ingredient, )
from users.models import Follow, User
from .serializers import (TagSerializer, RecipeSerializer,
                          RecipeCreateSerializer, IngredientSerializer,
                          FavoriteSerializer, FollowSerializer,
                          ShoppingCartSerializer, RecipeIngredient
                          )
from .filters import RecipeFilter, IngredientFilter


class TagViewSet(ModelViewSet):
    """Вьюсет для тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """Вьюсет для рецептов."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, ]
    pagination_class = PageNumberPagination
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorPermissions, ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False)
    def download_shopping_cart(self, request):
        ingredients = (RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit',).annotate(
            amount=Sum('amount')).order_by()
        )
        print(ingredients)
        data = []
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['amount']
            data.append(f'{name}: {amount}, {measurement_unit}\n')
        response = HttpResponse(content=data, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="cart.txt"'
        return response


class IngredientViewSet(ModelViewSet):
    """Вьюсет для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    permission_classes = [AllowAny, ]
    pagination_class = None


class Favorite(generics.RetrieveDestroyAPIView,
               generics.ListCreateAPIView):
    '''Вьюсет для добавления и удаления рецепта в избранное.'''
    queryset = Recipe.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return get_object_or_404(Recipe, id=self.kwargs['recipe_id'])

    def create(self, request, *args, **kwargs):
        '''Добавление в избранное.'''
        recipe = self.get_object()
        favorite = request.user.favorites.create(recipe=recipe)
        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        '''Удаление из избранного.'''
        self.request.user.favorites.filter(recipe=instance).delete()


class FollowersViewSet(generics.ListAPIView):
    """Вьюсет для отображения подписчиков."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['GET'])
    def subscriptions(self, request):
        '''Метод для отображения всех подписок пользователя.'''
        follows = request.user.follower
        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data)


class Follows(generics.RetrieveDestroyAPIView,
              generics.ListCreateAPIView):
    """Вьюсет для подписки или отписки."""
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        '''Создание подписки.'''
        user_author = get_object_or_404(User, id=self.kwargs['user_id'])
        follow = request.user.follower.create(author=user_author)
        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        '''Получение id пользователя из URL.'''
        user_id = self.kwargs['user_id']
        return get_object_or_404(User, id=user_id)

    def perform_destroy(self, instance):
        '''Удаление подписки.'''
        self.request.user.follower.filter(author=instance).delete()


class ShoppingCart(generics.RetrieveDestroyAPIView,
                   generics.ListCreateAPIView):
    """Вьюсет для добавления и удаления рецептов из листа покупок."""

    queryset = Recipe.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        '''Получение id рецепта из URL.'''
        return get_object_or_404(Recipe, id=self.kwargs['recipe_id'])

    def create(self, request, *args, **kwargs):
        '''Добавление в список покупок.'''
        recipe = self.get_object()
        request.user.shopping_cart.create(recipe=recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        '''Удаление из листа покупок.'''
        self.request.user.shopping_cart.filter(
            recipe=self.get_object()).delete()
