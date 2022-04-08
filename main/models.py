from django.db import models

from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True) #pk =true чтобы джанго не создавал поле первичный ключ
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts') # через слово posts сможем вытащить все посты
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=225)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PostImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True) #куда будет загружаться
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

