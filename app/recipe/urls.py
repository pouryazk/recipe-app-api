from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipe import views

# routers automatically generate urls for viewsets
router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('ingredient', views.IngredientViewSet)

app_name = 'recipe'  # required for reverse function

urlpatterns = [
    path('', include(router.urls)),
]
