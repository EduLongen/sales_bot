from django.contrib.auth import get_user_model
from django import forms
from .models import User, Message, PixPayment

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Senhas não conferem")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash password

        # If it's the first user, make them superuser and admin
        if User.objects.count() == 0:
            user.is_superuser = True
            user.is_staff = True
            user.role = 'administrator'
        else:
            user.role = 'moderator'  # Default role for other users

        if commit:
            user.save()
        return user

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'description', 'content'] 
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 5,
                'cols': 60,
                'placeholder': 'Digite sua mensagem aqui...',
            }),
            'created_at': forms.TextInput(attrs={'readonly': 'readonly'}),  
        }

class PixPaymentForm(forms.ModelForm):
    class Meta:
        model = PixPayment
        fields = ['pix_key']
        widgets = {
            'pix_key': forms.TextInput(attrs={
                'placeholder': 'Digite a chave Pix',
                'class': 'input-field',
            }),
        }