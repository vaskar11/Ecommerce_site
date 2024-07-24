from django import forms
from catalog.models import Product, Category
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#create a model form here

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'category','photo',)
            
class CategoryForm(ModelForm):
    class Meta:
        model= Category
        fields = ('name',) 
        
class SignupForm(UserCreationForm):
    class Meta:
        model= User
        fields= {'username','password1','password2'}

class LoginForm(forms.Form):
    username= forms.CharField()
    password= forms.CharField(widget= forms.PasswordInput)
    