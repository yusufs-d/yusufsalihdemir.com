from django.http import response
from django.shortcuts import redirect, render, HttpResponse,get_object_or_404
from django.urls import reverse
from .forms import ArticleForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Article, Comment

# Create your views here.

def index(request):
    
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def my_skills(request):
    return render(request,"my_skills.html")

def all_articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        return render(request,"all_articles.html",{"articles" : articles})
    articles = Article.objects.all()
    context = {
        "articles" : articles
    }
    return render(request,"all_articles.html",context)

def contact_me(request):
    articles = Article.objects.all()
    return render(request,"contact_me.html",{'articles':articles})

def detail(request,id):
    article = get_object_or_404(Article,id = id)
    comments = article.comments.all()
    return render(request, "detail.html",{"article" : article, "comments" : comments})

@staff_member_required()
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles" : articles
    }
    return render(request,"dashboard.html",context)

@staff_member_required()
def add_article(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Article successfully added!")
        return redirect("dashboard")

    context = {
        "form" : form
    }
    return render(request,"add_article.html",context)

@staff_member_required()
def update_article(request,id):
    article = get_object_or_404(Article,id = id)
    form = ArticleForm(request.POST or None, request.FILES or None,instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Article successfully updated!")
        return redirect("dashboard")

    context = {
        "form" : form
    }
    return render(request,"update.html",context)

@staff_member_required()
def delete_article(request,id):
    article = get_object_or_404(Article,id=id)
    article.delete()
    messages.success(request,"Article successfully deleted!")
    return redirect("dashboard")

@login_required(login_url="user:login")
def add_comment(request,id):
    article = get_object_or_404(Article,id=id)
    if request.method == "POST":
        comment_author = request.user
        comment_content = request.POST.get("comment_content")
        newComment = Comment(comment_author = comment_author,comment_content = comment_content)
        newComment.article = article
        newComment.save()
        messages.success(request,"Comment added successfully !")
    return redirect(reverse("article:detail",kwargs={"id":id}))