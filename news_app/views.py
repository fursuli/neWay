from django.contrib.auth.backends import ModelBackend
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic

from .forms import PostForm, UserForm, CommentForm
from .models import Post

from django.contrib.auth import get_user_model, login

from .tokens import account_activation_token

User = get_user_model()

def index(request):

    approved_posts = Post.objects.filter(moderation=True).count()
    not_approved_posts = Post.objects.filter(moderation=False).count()
    num_users = User.objects.all().count()

    context = {
        'approved_posts': approved_posts,
        'not_approved_posts': not_approved_posts,
        'num_users': num_users,
    }

    return render(request=request, template_name='newsApp/homePage.html', context=context)

def create_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if request.user.is_staff:
            instance.moderation = True
            instance.owner = request.user
            instance.save()
            return redirect(to='approved')
        instance.owner = request.user
        instance.save()
        return HttpResponse("New post need to be approved by moderators.")
    return render(request=request, template_name='newsApp/create_new.html', context={'form': form})


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.related_post = post
            comment.author = request.user
            comment.save()
            return redirect('post-details', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'newsApp/add_comment_to_post.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                       # .decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserForm()
    return render(request, 'registration/signUp.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('index')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class UserListView(generic.ListView):
    model = User
    context_object_name = 'user_list'
    template_name = 'newsApp/users.html'


    def get_queryset(self):
        return User.objects.all()

class UserDetailView(generic.DetailView):
    model = User
    template_name = 'newsApp/user_detail.html'


    def user_detail_view(request, primary_key):
        try:
            user = User.objects.get(pk=primary_key)
        except User.DoesNotExist:
            raise Http404('User does not exist')

        return render(request, 'newsApp/user_detail.html', context={'user': user})


class ApprovedPostListView(generic.ListView):
    model = Post
    context_object_name = 'a_posts_list'
    template_name = 'newsApp/approved_posts.html'

    ordering = ['-date_posted']

    def get_queryset(self):
        queryset = super(ApprovedPostListView, self).get_queryset()

        return queryset.filter(moderation=True)


class NotApprovedPostListView(generic.ListView):
    model = Post
    context_object_name = 'nota_posts_list'
    template_name = 'newsApp/not_approved.html'

    ordering = ['-date_posted']

    def get_queryset(self):
        queryset = super(NotApprovedPostListView, self).get_queryset()
        return queryset.filter(moderation=False)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'newsApp/post_detail.html'


    def post_detail_view(request, primary_key):
        try:
            post_id = Post.objects.get(pk=primary_key)
        except Post.DoesNotExist:
            raise Http404("Information does not exist")

        # post_id=get_object_or_404(Post, pk=primary_key)

        return render(request, 'newsApp/post_detail.html', context={'post': post_id})
