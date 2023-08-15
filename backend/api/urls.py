from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet, RecipeViewSet, IngredientViewSet,
                    Favorite, Follows, FollowersViewSet,
                    ShoppingCart, )

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'users/subscriptions/',
        FollowersViewSet.as_view(),
        name='subscriptions'),
    path(
        'users/<int:user_id>/subscribe/',
        Follows.as_view(),
        name='subscribe'),
    path(
        'recipes/<int:recipe_id>/favorite/',
        Favorite.as_view(),
        name='favorite'),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingCart.as_view(),
        name='shopping_cart'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
