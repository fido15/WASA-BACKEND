from django.urls import include, path
#Landry
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'Welcome',helloViewset, basename='welcome')
router.register(r'NewSite',NewSitesViewset,basename='NewSite')
router.register(r'RssData',DataRssViewset,basename='RssData')
router.register(r'Category',CategoryViewset,basename ='Category')
# Wire up our API using automatic URL routing.   
urlpatterns = [
    path('', include(router.urls)),
]