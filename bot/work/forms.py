from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Session
from django import forms
from django.core.validators import URLValidator
from django.forms import formset_factory


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль',
    }))


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'number', 'api_id', 'api_hash', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя',
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Почта',
    }))

    number = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Номер телефона',
            'type': 'tel'
        }),
        max_length=20,
        label='Телефон'
    )

    api_id = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'api_id',
    }))

    api_hash = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'api_hash',
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль',
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Повторите пароль',
    }))


class ChatLinkForm(forms.Form):
    link = forms.URLField(
        label='Ссылка на чат',
        widget=forms.URLInput(attrs={
            'placeholder': 'https://t.me/chatname'
        }),
        validators=[URLValidator()]
    )


ChatLinkFormSet = formset_factory(ChatLinkForm, extra=1, max_num=10)


class SessionStep1Form(forms.ModelForm):

    class Meta:
        model = Session
        fields = ('session', )

    session = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя ceссии',
    }))


class SessionStep2Form(forms.ModelForm):
    class Meta:
        model = Session
        fields = ('additional_field', )
        additional_field = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Введите код с телеграмма',
        }))