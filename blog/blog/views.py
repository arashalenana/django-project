# from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.
# def post_list(request):
#     posts=Post.objects.all()
#     return render(request, 'home.html', {'posts':posts})

# def post_detail(request, pk): #PK - primary key
#     post=get_object_or_404(Post, pk=pk)
#     return render(request, 'post_detail.html', {'post':post})

class BlogListView(ListView):
    model=Post
    template_name='home.html'
    context_object_name='posts'
class BlogDetailView(DetailView):
    model=Post
    template_name='post_detail.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['user']=self.request.user
        print(context['user'])
        return context
class BlogCreateView(CreateView):
    model=Post
    template_name='post_new.html'
    fields=['title', 'author', 'body']
class BlogUpdateView(UpdateView):
    model=Post
    template_name='post_edit.html'
    fields=['title', 'body']
class BlogDeleteView(DeleteView):
    model=Post
    template_name='post_delete.html'
    success_url=reverse_lazy('home')