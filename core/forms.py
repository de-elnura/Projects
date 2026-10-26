from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        required=True,
        label="Ism",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingizni kiriting'})
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        label="Familiya",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangizni kiriting'})
    )
    email = forms.EmailField(
        required=True,
        label="Email manzil",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@misol.uz'})
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        initial='student',
        label="Platformadagi rolingiz",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Foydalanuvchi nomi (username)'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Parol o\'ylab toping'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Parolni qaytadan kiriting'
        })


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username kiriting'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Parol kiriting'})
    )
