# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import generics, viewsets, status

# from main.models import Category, Post
# from main.serializers import CategorySerializer, PostSerializer
#
#
# # 'GET' -метод, к-ый доступен к представлению ниже
#
#
#
# @api_view(['GET']) #декоратор для того, чтоюы использовать ф-ю в REST API
# def categories(request):
#     if request.method == 'GET':
#         categories = Category.objects.all() #вытаскиваем все обьекты из Категории
#         serializer = CategorySerializer(categories, many=True) #в переменной сериал-р  хранится Сериал-р которые будет сериализовать данные
#                                                             #many - чтоб сери-р влючал несколько обьектов
#         return Response(serializer.data) #serializer.data, data -тут будут хранится данные в отформатированном виде, нам вернется ответ в виде json
#
#
# class PostListView(APIView):
#     def get(self, request):    #если поль-ль отправляет запрос методом get
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#
#     def post(self, request):
#         post = request.data.get('post')
#         serializer = PostSerializer(data=post)
#         if serializer.is_valid(raise_exception=True):
#             post_save = serializer.save()
#         return Response(serializer.data)
#

# 2й метод
from rest_framework.decorators import action
from rest_framework.response import Response
from main.models import Category, Post, PostImage
from main.serializers import CategorySerializer, PostSerializer, PostImageSerializer



# class PostListView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class PostView(generics.ListCreateAPIView): #создание поста
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
# class PostDetailView(generics.RetrieveAPIView): #страница детализации
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
# class PostUpdateView(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
# class PostDeleteView(generics.DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class CategoryListView(generics.ListAPIView):
    #наследуем от ListAPIView т.к. нам нужен весь список
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

 #action доступны только во viewset!!
    @action(detail=False, methods=['get'])    #router build path posts/search/?q=paris
    def search(self, request, pk=None):
        print(request.query_params)
        q = request.query_params.get('q')   #request.query_params = request.GET
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(text__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class PostImageView(generics.ListAPIView):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer

    def get_serializer_context(self):   #переопределяем метод
        return {'request': self.request}
