
#System imports
from django.urls import path , include
from rest_framework.routers import DefaultRouter

#Local Imports
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet , basename='product')
router.register(r'categories', CategoryViewSet)
urlpatterns = [
     path('' , include(router.urls))
]