from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet, RecipeViewSet, IngredientViewSet,
                    FavoriteViewSet, FollowViewSet, FollowersViewSet,
                    ShoppingCartViewSet, )

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('users/<int:id>/favorite/', FavoriteViewSet,
                   basename='favorite')
router_v1.register('users/<int:id>/subscribe/', FollowViewSet,
                   basename='follow')
router_v1.register('users/<int:id>/subscriptions/', FollowersViewSet,
                   basename='followers')
router_v1.register('users/<int:id>/shopping_cart/', ShoppingCartViewSet,
                   basename='shopping_cart')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router_v1.urls)),
]
