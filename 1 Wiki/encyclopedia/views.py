from django.shortcuts import render
from . import util
from markdown2 import markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def show_page(request,title):
    if title not in util.list_entries():
        message = "Entry not found"
        return render(request, "encyclopedia/error.html", {"message": message})
    else:
        content = markdown(util.get_entry(title))
        return render(request, "encyclopedia/page.html", {"content": content,"title":title})

def search(request):
    if request.method == "GET":
        query = request.GET.get("q")

        if query in util.list_entries():
            return HttpResponseRedirect(reverse("show_page", kwargs={'title': query}))
        else:
            results = []
            for entry in util.list_entries():
                if query in entry:
                    results.append(entry)

            return render(request, "encyclopedia/search.html", {"results": results})    

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    
    if request.method == "POST":
        title = request.POST.get("title")
        if title in util.list_entries():
            message = "Entry already exists"
            return render(request, "encyclopedia/error.html", {"message": message})
        else:
            content = request.POST.get("content")
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("show_page", kwargs={'title': title}))
        

def edit(request):
    if request.method == "GET":
        title = request.GET.get("title")
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"content": content,"title":title})

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("show_page", kwargs={'title': title}))

def random_page(request):
    if request.method == "GET":
        title = choice(util.list_entries())
        return HttpResponseRedirect(reverse("show_page", kwargs={'title': title}))
        