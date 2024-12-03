"""
Файл views.py для додатку blog.

Містить обробники запитів для роботи з постами та коментарями:
- Відображення списку постів.
- Відображення деталей поста з коментарями.
- Створення нових постів.
"""

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm, PostForm
from .models import Post, Category, Tag


def post_list(request):
    """
    Відображає список усіх постів.

    :param request: HTTP-запит.
    :return: HTTP-відповідь зі сторінкою списку постів.
    """
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    """
    Відображає деталі поста та обробляє створення коментарів.

    Додатково:
    - Якщо користувач авторизований, дозволяє створити коментар.
    - Надсилає автору поста email-сповіщення про новий коментар.

    :param request: HTTP-запит.
    :param pk: Первинний ключ поста.
    :return: HTTP-відповідь зі сторінкою деталей поста.
    """
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()

                # Відправка email автору поста
                send_mail(
                    'Новий коментар',
                    'До вашого поста додано новий коментар!',
                    'test_for_django@ukr.net',
                    [post.author.email],
                    fail_silently=False,
                )
                return redirect('post_detail', pk=post.pk)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form,
        'comments': comments,
    })


@login_required
def create_post(request):
    """
    Дозволяє зареєстрованим користувачам створювати нові дописи.

    Додатково:
    - Обробляє категорії та теги, які створюються або додаються до поста.
    - Перенаправляє на сторінку списку постів після успішного створення.

    :param request: HTTP-запит.
    :return: HTTP-відповідь зі сторінкою створення поста або перенаправлення.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Обробка категорій
            categories = form.cleaned_data['categories']
            if categories:
                category_objects = []
                for category_name in categories.split(','):
                    category_name = category_name.strip()
                    category_obj, created = Category.objects.get_or_create(name=category_name)
                    category_objects.append(category_obj)
                post.categories.set(category_objects)

            # Обробка тегів
            tags = form.cleaned_data['tags']
            if tags:
                tag_objects = []
                for tag_name in tags.split(','):
                    tag_name = tag_name.strip()
                    tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                    tag_objects.append(tag_obj)
                post.tags.set(tag_objects)

            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})
