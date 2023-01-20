from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', MainView.as_view(), name='home'),
    path('blog/<slug>/', PostDetailView.as_view(), name='post_detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/signup_success', SignUpSuccessView.as_view(), name='signup_success'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout',),
    path('contact/', FeedBackView.as_view(), name='contact'),
    path('contact/success/', SuccessView.as_view(), name='success'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('tag/<slug:slug>/', TagView.as_view(), name="tag"),
    path('comments/<int:pk>/', AddComment.as_view(), name='add_comment'),
    path("password_reset_form", PasswordReset.as_view(), name="password_reset_form"),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='myblog/password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="myblog/password/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='myblog/password/password_reset_complete.html'),
         name='password_reset_complete'),
]


