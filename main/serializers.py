from rest_framework import serializers

from .models import Category, Post, PostImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True) #будет выходить по умолчанию чисто для чтения

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'author', 'text', 'created_at')
    def to_representation(self, instance):  #этот метод отвечает за то в какм виде полуим ответ
        representation = super().to_representation(instance)
        representation['images'] = PostImageSerializer(instance.images.all(),
                                                     many=True, context=self.context).data
        return representation


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

    def _get_image_url(self, obj):  #для картинки в Postman
         if obj.image:
             url = obj.image.url
             request = self.context.get('request')
             if request is not None:   #если запрос не пустой
                url = request.build_absolute_uri[url]       #то мы переопределяем url методом uri
         else:
                url = ''
         return url
    def to_representation(self, instance): #переопределим, чтобы
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance) #в instance заходит объект модельки PostImage
        return representation


