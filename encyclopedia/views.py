from os import close
from re import template
from django.http.response import HttpResponse
from django.shortcuts import render
import markdown2
from . import util
from django.http import HttpResponseRedirect
from django import forms
import os.path
import random

class MakeFrom(forms.Form):
    """ Form Class for Creating New Entries """
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "placeholder": "Page Title"}))

    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        "rows":3, "cols":50,
      "placeholder": "Enter Page Content using Github Markdown"
    }))

class SearchForm(forms.Form):
    value = forms.CharField(label='', widget=forms.TextInput(attrs={
      "placeholder": "Search my wiki"}))

def index(request):
    if request.POST:
        form = SearchForm(request.POST)
        close = []
        if form.is_valid():
            entries = util.list_entries()
            value = form.cleaned_data['value'].lower()
            for entry in entries :
                if entry.lower() == value:
                    return HttpResponseRedirect(f'/{value}')
                elif entry.lower() in value or value in entry.lower() :
                    close.append(entry)
            if len(close) > 0 : 
                form = SearchForm()
                return render(request, "encyclopedia/index.html", {
                "entries":close,
                'form': form})
            else:
                return HttpResponseRedirect(f'/{value}')

        else:
            form = SearchForm()
            return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            'form': form})
    else:
        form = SearchForm()
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            'form': form
    })

def get(request,title):
    form = SearchForm()
    check = util.get_entry(title)
    if check :
        html = markdown2.markdown(check)
        return render(request, "encyclopedia/entry.html",{
        "title" : title,
        "content" : html,
        "exsists" : 1,
        "form":form
        })
    else:
        return render(request,"encyclopedia/entry.html",{
        "title" : title,
        "exsists" : 0,
        "form":form
        })
def make(request):
    if request.POST:
        form1 = MakeFrom(request.POST)
        form = SearchForm()
        # check whether it's valid:
        if form1.is_valid():
            title = form1.cleaned_data['title']
            text = form1.cleaned_data['text']
            save_path = ("C:/Users/HAREL/django/wiki/entries")
            complete_path =os.path.join(save_path,title +".md")   
            f = open(complete_path, "a")
            f.write(f"# {title} \n {text}")
            f.close()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # url index insted of thanks 
            return HttpResponseRedirect('/')
    else:
        form1 = MakeFrom()
        form = SearchForm()

    return render(request, 'encyclopedia/make.html', {'form1': form1 ,'form':form})


def randoms(request):
    pages = util.list_entries()
    page = random.choice(pages)
    return HttpResponseRedirect(f"/{page}")

