from django.shortcuts import render
import markdown
import random
from . import util

#convert markdown to html
def convert_md(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request,title):
    html_content = convert_md(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            entries = util.list_entries()
            recommended_search = []
            for entry in entries:
                if entry_search.lower() in entry.lower():
                    recommended_search.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation" : recommended_search
            })
        
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        title_exist = util.get_entry(title)
        if title_exist is not None:
            return render(request, "encyclopedia/error.html", {
                "message" : "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })
        
def edit(request):
    if request.methon == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.methon == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })


def rand(request):
    entries = util.list_entries() 
    if not entries:
        return render(request, "encyclopedia/error.html", {
            "message": "No entries available"
        })
    random_entry = random.choice(entries)
    html_content = convert_md(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })

        


            


