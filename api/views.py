from django.shortcuts import render
from inventory.models import ProductInventory
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator

# ესეიგი ეს ყველაფერი გვჭირდება ეიპიაისთვის

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)

from .serializers import *

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


# class bookApi(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
#     # მოკლედ ეს ორი გვჭირდება აუცილებლად სერიალაიზერ კლასი და მონაცემები
#     queryset = Book.objects.all().order_by('id')
#     serializer_class = bookSerializer
#     permission_classes = []
#     pagination_class = StandardResultsSetPagination

#     # ესენი უკვე რაღაც ფუნქციაებია რომელიც იგივე რაღაცეებს აკეთებს
#     # @method_decorator(cache_page(60 * 15))
#     def get(self, request: Request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     # @method_decorator(cache_page(60 * 15))
#     def post(self, request: Request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance
class ProductDetailAPIView(generics.ListAPIView):
    serializer_class = ProductInventorySerializer
    queryset = ProductInventory.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        search_query = self.kwargs.get('search', '')

        #ვანაწევრებთ სიტყვას რათა უფრო მრავალმხრივად დავსერჩოთ
        search_terms = search_query.split()
        
        # ამით ვაკეთებ ქუერიებს უბრალოდ __icontains ამის დახმარებით ვეძებთ თითოეული ტერმინისთვის
        # ვაკავშირებთ AND ოპერატორით რათა ვნახოთ სიტყვებიდან თუ არის სათაურში რომელიმე თუ ორივეა
        # მაშინ მთლიანი სიტყვით დაისერჩება ანუ მაგალთად harry potter
        # Using Q objects to create OR condition for each search term
        title_queries = [Q(product__name__icontains=term) for term in search_terms]
        author_queries = [Q(product__description__icontains=term) for term in search_terms]

        # ანუ მარტივად რო ვთქვათ ეხლა ჩვენ ვეძებთ გახლეჩილი ქუერით ანუ თუ ქუერი იქნებოდა
        # harry potter ჩვენ ამას გავხლიჩავთ ['harry', 'potter'] და შემდეგ მოვძებნით ორივე სიტყვის გამოყენებით
        # ანუ თუ სათაური ერგება ჰარის ან პოტერს ან ორივეს ერთად და იგივე ავტორზეც
        # ესეიგი ეხლა ჩვენ გვაქ წიგნები და ავტორები რომლებიც შეიცავენ ჰარის ან პოტერს ან ორივეს ერთად
        # Combining OR conditions for each field
        title_q = Q(*title_queries, _connector=Q.OR)
        author_q = Q(*author_queries, _connector=Q.OR)

        # Using SearchVector, SearchQuery, SearchRank for searching in title and authors
        vector = SearchVector('product__name', 'product__description')
        # ანუ ეს არის ქუერი რითიც ვეძებთ
        query = SearchQuery(search_query)
        # ეს გამოთვლის რამდენად ემთხვევიან ფიელდები და სერჩ ქუერი
        rank = SearchRank(vector, search_query)

        # Using TrigramSimilarity for searching in title and authors
        trigram_similarity_title = TrigramSimilarity('product__name', search_query)
        trigram_similarity_authors = TrigramSimilarity('product__description', search_query)
        # Performing the combined search
        results = ProductInventory.objects.annotate(
            rank=rank,
            trigram_similarity_title=trigram_similarity_title,
            trigram_similarity_authors=trigram_similarity_authors,
        ).filter(
            title_q | author_q
        ).order_by('-rank', '-trigram_similarity_title', '-trigram_similarity_authors')

        return results