from django.shortcuts import render, get_list_or_404,redirect,HttpResponse,HttpResponseRedirect, get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment, Vote
from django.views.generic import DetailView
from .forms import PostForm,SignUpForm, CommentForm
from django.urls import reverse_lazy,reverse
from django.views.generic import (
    TemplateView, CreateView,
    ListView,DetailView,
    UpdateView,DeleteView,
)

class ListPosts(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/list_posts.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class CreatePost(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_form.html'
    model = Post
    form_class = PostForm
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['value'] = 'Create'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class DetailPost(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post = self.get_object()

        # Get user's vote status
        if user.is_authenticated:
            vote = Vote.objects.filter(post=post, author=user).first()
            context['user_vote'] = vote.vote if vote else None
        else:
            context['user_vote'] = None  # Not logged in

        # Add upvote/downvote count
        context['total_upvotes'] = post.total_upvotes()
        context['total_downvotes'] = post.total_downvotes()

        # Add comment form to context
        context['comment_form'] = CommentForm()

        return context


class DraftPosts(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/draft_posts.html'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by("created_date")

class UpdatePost(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Post
    form_class = PostForm

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['value'] = 'Update'
        return context

class DeletePost(LoginRequiredMixin,DeleteView):
    login_url = '/login/'
    model = Post
    template_name = 'blog/confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('posts')


@login_required(login_url='/login/')
def post_publish(request,pk):
    post = get_list_or_404(Post,pk=pk)[0]
    post.publish()
    return redirect('blog:detail',pk=pk)

############# login_signup #############

def sign_up(request):
    registered = False

    if request.method == 'POST':
        user_form = SignUpForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        
        else:
            print(user_form.errors)
    else:
        user_form = SignUpForm()   
    return render(request,'blog/auth/signup.html',{'user_form': user_form,
                                                          'registered': registered
                                                          })
                                                          
def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('posts')
        else:
            return HttpResponse("Invalid Username or Password ..")
    return render(request,'blog/auth/login.html',{})
        
@login_required
def log_out(request):
    logout(request)
    return redirect('posts')
        
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:detail', pk=post.pk)  # Ensure this matches 'detail' in your URLs

    return redirect('blog:detail', pk=post.pk)


@login_required
def vote_post(request, pk, vote_type):
    post = get_object_or_404(Post, pk=pk)
    existing_vote = Vote.objects.filter(post=post, author=request.user).first()

    if existing_vote:
        if existing_vote.vote == vote_type:
            existing_vote.delete()  # Remove vote if clicking the same button again
        else:
            existing_vote.vote = vote_type  # Change vote type
            existing_vote.save()
    else:
        Vote.objects.create(post=post, author=request.user, vote=vote_type)

    return redirect('blog:detail', pk=pk)