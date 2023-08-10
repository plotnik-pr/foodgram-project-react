from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet, RecipeViewSet, IngredientViewSet,
                    FavoriteViewSet, FollowViewSet, FollowersViewSet,
                    ShoppingCartViewSet, )

app_name = 'api'

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'favorite', FavoriteViewSet, basename='favorite')
router.register(r'subscribe', FollowViewSet, basename='follow')
router.register(r'subscriptions', FollowersViewSet, basename='followers')
router.register(r'recipes', ShoppingCartViewSet, basename='shopping_cart')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
