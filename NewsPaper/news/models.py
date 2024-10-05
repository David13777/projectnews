from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.core.cache import cache
from django.utils.translation import pgettext_lazy


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.posts.aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = self.user.comments.aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        post_comments_rating = self.posts.aggregate(pcr=Coalesce(Sum('comment__rating'), 0))['pcr']


        self.rating = posts_rating * 3 + comments_rating + post_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')


    def __str__(self):
        return self.name


class Post(models.Model):
    news = "NW"
    articles = "AR"

    POST_TYPES = [
        (news, "Новость"),
        (articles, "Статья")
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=news)
    date_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."

    def __str__(self):
        return f'id-{self.pk}: {self.title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    date_in = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    kind = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='kinds',
        verbose_name=pgettext_lazy('help text for MyModel model', 'This is the help text'),
    )