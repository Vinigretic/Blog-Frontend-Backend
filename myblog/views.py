from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.core.paginator import Paginator
from .models import Post
from .forms import *
from django.contrib.auth import login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from taggit.models import Tag
from django.utils.translation import gettext
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


class MainView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'myblog/home.html', context={
            'page_obj': page_obj
        })


class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-id')[:3]
        comment_form = CommentForm()
        return render(request, 'myblog/post_detail.html', context={
            'post': post,
            'common_tags': common_tags,
            'last_posts': last_posts,
            'comment_form': comment_form
    })


class AddComment(View):
    def post(self, request, pk):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(id=pk)
        username = self.request.user
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            if request.POST.get('parent', None):
                comment_form.parent_id = int(request.POST.get('parent'))
            comment_form.post = post
            comment_form.username = username
            comment_form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'myblog/post_detail.html', context={
            'comment_form': comment_form
        })


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SigUpForm()
        return render(request, 'myblog/signup.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SigUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                subject = 'Confirmation of registration'
                email_template_name = "myblog/signup_success.txt"
                c = {
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Website',
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                send_mail(subject, email, 'bakatvita@gmail.com', [user.email], fail_silently=False)
                return HttpResponseRedirect('signup_success')
        return render(request, 'myblog/signup.html', context={
            'form': form,
        })


class SignUpSuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'myblog/signup_success.html', context={
            'title': gettext('На ваш email была отправлена ссылка. Для завершения регистрации пройдите по этой ссылке.')
        })


class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'myblog/signin.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username'].lower()
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'myblog/signin.html', context={
            'form': form,
        })


class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'myblog/contact.html', context={
            'form': form,
            'title': gettext('Чтобы связаться со мной, заполните форму обратной связи.')
        })

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | topic: {subject} | email: {from_email}', message, from_email, ['bakatvita@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'myblog/contact.html', context={
            'form': form,
        })


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'myblog/success.html', context={
            'title': gettext('Ваше письмо отправлено! Спасибо!')
        })


class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        results = ""
        if query:
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
            )
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'myblog/search.html', context={
            'title': 'Поиск',
            'results': page_obj,
            'count': paginator.count
        })


class TagView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()
        return render(request, 'myblog/tag.html', context={
            'title': f'#ТЕГ {tag}',
            'posts': posts,
            'common_tags': common_tags
        })


class PasswordReset(View):
    def get(self, request, *args, **kwargs):
        reset_form = ResetForm()
        return render(request, 'myblog/password/password_reset_form.html', context={
            'form': reset_form,
        })


    def post(self, request, *args, **kwargs):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            data = reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "myblog/password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'bakatvita@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
            else:
                return redirect("/password_reset/done/")
        return render(request=request, template_name="myblog\password/password_reset_form.html", context={"form":reset_form})

