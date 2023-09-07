from django.shortcuts import render

from . import util
from markdown2 import Markdown
import random

def convert_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def  entry(request, title, ):
    html_content = convert_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "error": "Page not found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def search(request):
    query = request.POST.get('q')
    if query in util.list_entries():
        return entry(request, query)
    else:
        entries = []
        for entry in util.list_entries():
            if query.lower() in entry.lower():
                entries.append(entry)
        return render(request, "encyclopedia/search.html", {
            "entries": entries
        })



def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        existing_files = util.list_entries()
        if title.lower() in [entry.lower() for entry in existing_files]:
            return render(request, "encyclopedia/error.html", {
                "error": "Page already exists"
            })
        if title == "" or content == "":
            return render(request, "encyclopedia/error.html", {
                "error": "Title or content empty"
            })
        else:
            util.save_entry(title, content)
            return entry(request, title)
    else:
        return render(request, "encyclopedia/create.html")


def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        } )
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
def rand(request):
    entries = util.list_entries()
    rand_entry = random.choice(entries)
    html_content = convert_to_html(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content": html_content
        })