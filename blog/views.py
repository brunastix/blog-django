from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from .models import Post

class PostListView(ListView):
    model = Post
    paginate_by = 6

    def get_queryset(self):
        posts = super().get_queryset().select_related('author')
        query = self.request.GET.get('q', '').strip()
        return posts.filter(Q(title__icontains=query) | Q(content__icontains=query)) if query else posts

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AuthorPostsMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class PostUpdateView(AuthorPostsMixin, UpdateView):
    model = Post
    form_class = PostForm

class PostDeleteView(AuthorPostsMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.save())
        return redirect('post_list')
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html', {'posts': request.user.posts.all()})
