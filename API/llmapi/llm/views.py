from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from urllib.parse import urlparse
from .models import NewSite
from .models import RssData
from .models import Category
from rest_framework import status 
import os 
import feedparser
from .helpers import get_article_images
from .langchainservice import AIHelper
# Create your views here.

ai = AIHelper()



class helloViewset(ViewSet):
    def list(self, request):
        return Response({"MESSAGE": "Welcome to api "})


class CategoryViewset(ViewSet):

    def create (self,request):

        try:
            base_dir = os.path.dirname(__file__)
            file_path = os.path.join(base_dir,"category.txt")
            with  open(file_path,"r") as file :
                categories = file.readlines()
            for  category in categories:
                category = category.strip()
                if not Category.objects.filter(name=category).exists():
                    Category.objects.create(
                        name = category
                    )
            
            return Response({"message": "categories ajoutées avec succès dans NewSite !"}, status=status.HTTP_201_CREATED)

        except FileNotFoundError:
            return Response({"message":"le fichier  est manquant"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e :
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                  



class NewSitesViewset(ViewSet):

    def create(self,request):
        try:
            base_dir = os.path.dirname(__file__)
            file_path = os.path.join(base_dir, "link.txt")
            with open(file_path,"r") as file :
                links = file.readlines()

            for link in links:
                link = link.strip()
                parse_url = urlparse(link)
                source = parse_url.netloc

                if not NewSite.objects.filter(link=link).exists():
                    NewSite.objects.create(
                        link = link,
                        reliability= 0.0,
                        source = source
                    )
            return Response({"message": "Sites ajoutés avec succès dans NewSite !"}, status=status.HTTP_201_CREATED)

        except FileNotFoundError:
            return Response({"message":"le fichier  est manquant"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e :
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            


class DataRssViewset(ViewSet):

    def create(self,request):
        '''
        cette fonction permet de recuperer les donnes rss et de les stoker en base de donnes 
        '''
        try:
            print("debut")
            links = NewSite.objects.values_list('link',flat=True)
            for link in links :
                link = link.strip()
                feed = feedparser.parse(link)

                for entry in feed.entries:
                   # img = get_article_images(entry.get("link"))
                    if not RssData.objects.filter(title=entry.get("title")).exists():
                        country= ai.Country(entry.get("summary"))
                       
                        RssData.objects.create(
                            title=entry.get("title", ""),
                            link=entry.get("link", ""),
                            published=entry.get("published", None),
                            updated=entry.get("updated", None),
                            summary=entry.get("summary", ""),
                            country=country or "Unknow",
                            image =img[1:]
                        )
                       
        
                return Response({"message": "Données RSS chargées avec succès !"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
