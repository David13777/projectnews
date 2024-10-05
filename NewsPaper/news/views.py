from allauth.core.internal.http import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, MyModel, Author
from django.utils import timezone
from django.shortcuts import redirect
from django.http.response import HttpResponse #  импортируем респонс для проверки текста
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions

from django.utils.translation import gettext as _ #  импортируем функцию для перевода

import pytz

from .forms import PostForm
from .models import Post, Category
from .filters import PostFilter
from .serializers import PostSerializer, AuthorSerializer


class Index(View):
    def get(self, request):
        curent_time = timezone.now()

        # .  Translators: This message appears on the home page only
        models = MyModel.objects.all()

        context = {
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'index.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


class NewsList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = '-date_in'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'post'


class NewsSearch(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    permission_required = ('news.add_post',
                          'news.change_post')



class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.change_post')



class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = '/news/'


def author_now(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        user.groups.add(author_group)
    return redirect('post_list')


class CategoryListView(NewsList):
    model = Post
    template_name = 'category_List.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.ad(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return  render(request, 'news/subscribe.html', {'category': category, 'message': message})


def invalid_form(request):
    return render(request, template_name='views/invalid_create_form.html', context={'username': request.user.username})


class CheckView(View):

    def get(self,request):
        return HttpResponse('Hello')


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PostNewsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='NW')
    serializer_class = PostSerializer


class PostArticlesViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(post_type='AR')
    serializer_class = PostSerializer