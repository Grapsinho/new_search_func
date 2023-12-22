from django.shortcuts import render
from .models import Book
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


class bookApi(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    # მოკლედ ეს ორი გვჭირდება აუცილებლად სერიალაიზერ კლასი და მონაცემები
    queryset = Book.objects.all().order_by('id')
    serializer_class = bookSerializer
    permission_classes = []
    pagination_class = StandardResultsSetPagination

    # ესენი უკვე რაღაც ფუნქციაებია რომელიც იგივე რაღაცეებს აკეთებს
    # @method_decorator(cache_page(60 * 15))
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    # @method_decorator(cache_page(60 * 15))
    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.db.models import Q
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance
class BookDetailAPIView(generics.ListAPIView):
    serializer_class = bookSerializer
    queryset = Book.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        search_query = self.kwargs.get('search', '')

        #ვანაწევრებთ სიტყვას რათა უფრო მრავალმხრივად დავსერჩოთ
        search_terms = search_query.split()
        
        # ამით ვაკეთებ ქუერიებს უბრალოდ __icontains ამის დახმარებით ვეძებთ თითოეული ტერმინისთვის
        # ვაკავშირებთ AND ოპერატორით რათა ვნახოთ სიტყვებიდან თუ არის სათაურში რომელიმე თუ ორივეა
        # მაშინ მთლიანი სიტყვით დაისერჩება ანუ მაგალთად harry potter
        # Using Q objects to create OR condition for each search term
        title_queries = [Q(title__icontains=term) for term in search_terms]
        author_queries = [Q(authors__icontains=term) for term in search_terms]

        # ანუ მარტივად რო ვთქვათ ეხლა ჩვენ ვეძებთ გახლეჩილი ქუერით ანუ თუ ქუერი იქნებოდა
        # harry potter ჩვენ ამას გავხლიჩავთ ['harry', 'potter'] და შემდეგ მოვძებნით ორივე სიტყვის გამოყენებით
        # ანუ თუ სათაური ერგება ჰარის ან პოტერს ან ორივეს ერთად და იგივე ავტორზეც
        # ესეიგი ეხლა ჩვენ გვაქ წიგნები და ავტორები რომლებიც შეიცავენ ჰარის ან პოტერს ან ორივეს ერთად
        # Combining OR conditions for each field
        title_q = Q(*title_queries, _connector=Q.OR)
        author_q = Q(*author_queries, _connector=Q.OR)

        # Using SearchVector, SearchQuery, SearchRank for searching in title and authors
        vector = SearchVector('title', 'authors')
        # ანუ ეს არის ქუერი რითიც ვეძებთ
        query = SearchQuery(search_query)
        # ეს გამოთვლის რამდენად ემთხვევიან ფიელდები და სერჩ ქუერი
        rank = SearchRank(vector, search_query)

        # Using TrigramSimilarity for searching in title and authors
        trigram_similarity_title = TrigramSimilarity('title', search_query)
        trigram_similarity_authors = TrigramSimilarity('authors', search_query)

        # ანუ გააფერადებს იმ სიტყვებს რომელიც მოერგო ჩვენს ქუერის
        title_headline = SearchHeadline("title", query, start_sel='<span class="red_text">', stop_sel='</span>')
        author_headline = SearchHeadline("authors", query, start_sel='<span class="blue_text">', stop_sel='</span>')
        # Performing the combined search
        results = Book.objects.annotate(
            rank=rank,
            trigram_similarity_title=trigram_similarity_title,
            trigram_similarity_authors=trigram_similarity_authors,
            title_headline=title_headline,
            author_headline=author_headline
        ).filter(
            title_q | author_q
        ).order_by('-rank', '-trigram_similarity_title', '-trigram_similarity_authors')

        return results