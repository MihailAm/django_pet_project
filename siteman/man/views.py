from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from django.core.cache import cache

from .forms import AddPostForm, UploadFilesForm
from .models import Man, Category, TagPost, UploadFiles
from .utils import DataMixin


class ManHome(DataMixin, ListView):
    model = Man
    template_name = 'man/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        m_lst = cache.get('man_posts')
        if not m_lst:
            m_lst = Man.published.all().select_related('cat')
            cache.set('man_posts', m_lst, 60)

        return m_lst


@login_required
def about(request):
    contact_list = Man.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'man/about.html', {'title': 'О сайте', 'page_obj': page_obj})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class ShowPost(DataMixin, DetailView):
    template_name = 'man/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Man.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'man/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'
    permission_required = 'man.add_man'

    def form_valid(self, form):
        m = form.save(commit=False)
        m.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Man
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'man/addpage.html'
    success_url = reverse_lazy('home')
    permission_required = 'man.change_man'

    title_page = 'Редактирование статьи'


@permission_required(perm='man.view_man', raise_exception=True)
def contact(request):
    return HttpResponse(f"Обратная связь")


def login(request):
    return HttpResponse(f"Авторизация")


class ManCategory(DataMixin, ListView):
    template_name = 'man/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Man.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk)


class ManTag(DataMixin, ListView):
    template_name = 'man/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Man.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
                                      title=f"Тег: {tag.tag}")
