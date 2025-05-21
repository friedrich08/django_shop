from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser, Product, Category, Role


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  # Exclure 'roles'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        # Définir le rôle 'user' par défaut
        try:
            user_role = Role.objects.get(role_name='user')
            user.roles = user_role
        except Role.DoesNotExist:
            # Créer le rôle 'user' s'il n'existe pas
            user_role = Role.objects.create(role_name='user')
            user.roles = user_role
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    roles = forms.ModelChoiceField(
        queryset=Role.objects.filter(role_name__in=['user', 'admin']),
        empty_label=None,
        label="Rôle",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'roles']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Cet email n'existe pas.")

            self.user_cache = authenticate(self.request, username=user.username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Mot de passe incorrect.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("Ce compte est désactivé.")

        return self.cleaned_data


from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['pro_name', 'pro_price', 'pro_desc', 'category', 'user', 'image']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['cat_name']
        widgets = {
            'cat_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie',
            }),
        }
        labels = {
            'cat_name': 'Nom de la catégorie',
        }

    def clean_cat_name(self):
        cat_name = self.cleaned_data.get('cat_name')
        if Category.objects.filter(cat_name__iexact=cat_name).exists():
            raise forms.ValidationError("Une catégorie avec ce nom existe déjà.")
        return cat_name