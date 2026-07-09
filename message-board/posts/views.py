# from django.shortcuts import render
# from .models import Posts
# # Create your views here.
# def post_list(request):
#     posts=Posts.objects.all() #Selecting from all
#     return render(request,'post_list.html', {'posts':posts})

from django.views.generic import ListView
from .models import Posts
class PostList(ListView):
    model=Posts
    template_name='post_list.html'