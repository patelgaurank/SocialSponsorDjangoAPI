from django.urls import path
from .views import CategoryData
from rest_framework.routers import DefaultRouter

app_name = 'navbar'
router = DefaultRouter()
router.register('category', CategoryData,
                basename='category')
# urlpatterns = [
#     path('', CategoryData, name="Category_Data"),
# ]
urlpatterns = router.urls