# news/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Article
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def index(request):
    article_list = Article.objects.filter(is_published=True)
    paginator = Paginator(article_list, 10)  # Show 10 articles per page

    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        articles = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        articles = paginator.page(paginator.num_pages)

    return render(request, 'news/index.html', {'articles': articles})

def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    return render(request, 'news/article_detail.html', {'article': article})

# news/views.py
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    
    # Increment the views each time the article is viewed
    article.views += 1
    article.save()

    return render(request, 'news/article_detail.html', {'article': article})

@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        text = request.POST.get('text', '')
        Comment.objects.create(article=article, user=request.user, text=text)

    return redirect('article_detail', article_id=article_id)

@login_required
def add_like(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'POST':
        Like.objects.create(article=article, user=request.user)

    return redirect('article_detail', article_id=article_id)

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'news/user_login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'news/user_register.html', {'form': form})