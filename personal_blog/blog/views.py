from django.shortcuts import render, get_object_or_404, redirect
from .form import CommentForm
from .models import Post, Profile
from django.contrib import messages
from .form import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.paginator import Paginator




# Create your views here.
def index(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        posts = Post.objects.all().order_by('created_at')

    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'query': query}

    return render(request, 'blog/index.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    comment_form = None

    if request.user.is_authenticated and request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()

    context = {
        "post": post,
        "comment_form": comment_form,
    }
    return render(request, "blog/post-detail.html", context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()