from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet, RecipeViewSet, IngredientViewSet,
                    FavoriteViewSet, Follows, FollowersViewSet,
                    ShoppingCartViewSet, )

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'users/(?P<user_id>\d+)/favorite/',
                   FavoriteViewSet,
                   basename='favorite')
router_v1.register(r'users/(?P<user_id>\d+)/subscriptions/',
                   FollowersViewSet,
                   basename='followers')
router_v1.register(r'users/(?P<user_id>\d+)/shopping_cart/',
                   ShoppingCartViewSet,
                   basename='shopping_cart')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router_v1.urls)),
    path(
        'users/<int:user_id>/subscribe/',
        Follows.as_view(),
        name='subscribe'),
]
