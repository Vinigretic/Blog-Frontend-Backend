from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy


from .models import *


class SigUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
            'placeholder': gettext_lazy("Имя пользователя")
        }),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': "form-control",
            'id': "inputEmail",
            'placeholder': 'Email'
        }),
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "inputPassword",
            'placeholder': gettext_lazy("Пароль")
        }),
    )

    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'id': "ReInputPassword",
            'placeholder': gettext_lazy('Повторите пароль')
        }),
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(gettext_lazy('Такое имя пользователя уже существует'))
        elif User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(gettext_lazy('Пользователь с таким Email уже существует'))
        elif password != confirm_password:
            raise forms.ValidationError(
                gettext_lazy("Пароли не совпадают")
            )


    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'].lower(),
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "inputUsername",
            'placeholder': gettext_lazy("Имя пользователя")
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': "form-control mt-2",
            'id': "inputPassword",
            'placeholder': gettext_lazy("Пароль")
        })
    )

    def clean(self):
        username = self.cleaned_data.get('username').lower()
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError(gettext_lazy('Вы ввели некорректное имя пользователя или пароль'))


class FeedBackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'placeholder': gettext_lazy("Ваше имя")
        })
    )
    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': gettext_lazy("Ваша почта")
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'subject',
            'placeholder': gettext_lazy("Тема")
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control md-textarea',
            'id': 'message',
            'rows': 2,
            'placeholder': gettext_lazy("Ваше сообщение")
        })
    )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class ResetForm(forms.Form):
    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'inputEmail',
            'placeholder': 'Email'
        })
    )

