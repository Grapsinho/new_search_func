from django.shortcuts import render
from inventory.models import ProductInventory

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
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500


from django.core.cache import cache
class ProductInventoryApi(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    # მოკლედ ეს ორი გვჭირდება აუცილებლად სერიალაიზერ კლასი და მონაცემები
    queryset = ProductInventory.objects.all().order_by('id')
    serializer_class = ProductInventorySerializer
    permission_classes = []
    pagination_class = StandardResultsSetPagination

    # ესენი უკვე რაღაც ფუნქციაებია რომელიც იგივე რაღაცეებს აკეთებს
    # @method_decorator(cache_page(60 * 15))
    def get(self, request: Request, *args, **kwargs):
        cache_key = f"product_inventory_api_{request.GET.urlencode()}"
        cached_data = cache.get(cache_key)
        
        if not cached_data:
            response = self.list(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60 * 15)  # Cache for 15 minutes
            return response
        else:
            return Response(cached_data)
    
    # @method_decorator(cache_page(60 * 15))
    def post(self, request: Request, *args, **kwargs):
        cache.clear()
        return self.create(request, *args, **kwargs)

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.db.models import Q, F
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance
from django.db.models import Prefetch
# from django.core.cache import cache
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator

class ProductDetailAPIView(generics.ListAPIView):
    serializer_class = ProductInventorySerializer
    queryset = ProductInventory.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        search_query = self.kwargs.get('search', '')

        search_terms = search_query.split()
        
        # Using Q objects to create OR condition for each search term
        title_queries = [Q(product__name__icontains=term) for term in search_terms]
        author_queries = [Q(product__description__icontains=term) for term in search_terms]

        # Combining OR conditions for each field
        title_q = Q(*title_queries, _connector=Q.OR)
        author_q = Q(*author_queries, _connector=Q.OR)

        # Using SearchVector, SearchQuery, SearchRank for searching in title and authors
        vector = SearchVector('product__name', 'product__description')
        # ანუ ეს არის ქუერი რითიც ვეძებთ
        query = SearchQuery(search_query)
        rank = SearchRank(vector, search_query)

        # # Using TrigramSimilarity for searching in title and authors
        trigram_similarity_title = TrigramSimilarity("product__name", search_query)
        trigram_similarity_authors = TrigramSimilarity("product__description", search_query)

        prefetch_for_media = Prefetch('media_product_inventory', queryset=Media.objects.all())
        prefetch_for_product = Prefetch('product', queryset=Product.objects.all())
        
        # #Performing the combined search
        results = ProductInventory.objects.annotate(
            rank=rank,
            trigram_similarity_title=trigram_similarity_title,
            trigram_similarity_authors=trigram_similarity_authors,
        ).filter(
            title_q | author_q
        ).prefetch_related(prefetch_for_product, prefetch_for_media).only("id", "retail_price", "product__name", "product__description", "media_product_inventory__image").order_by('-rank', '-trigram_similarity_title', '-trigram_similarity_authors')

        return results