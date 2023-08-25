from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (Favorite, FollowersViewSet, Follows,
                    IngredientViewSet, RecipeViewSet,
                    ShoppingCart, TagViewSet)


app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
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
