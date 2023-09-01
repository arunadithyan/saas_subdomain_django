from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Profile, Tag, Article
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required


# Django Q objects use to create complex queries
# https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q-objects
from django.db.models import Q
from django_tenants.utils import remove_www
from tenant.models import Domain
def home(request):
    return render(request,'home.html')

def index(request):
    hostname_without_port = remove_www(request.get_host().split(':')[0])
    domain = Domain.objects.get(domain=hostname_without_port)
    name = domain.tenant.blog_name

    # feature articles on the home page
    featured = Article.articlemanager.filter(featured=True)[0:3]

    context = {
        'name':name,
        'articles': featured
    }

    return render(request, 'index.html', context)

@login_required
def articles(request):

    # get query from request
    query = request.GET.get('query')
    # print(query)
    # Set query to '' if None
    if query == None:
        query = ''

    # articles = Article.articlemanager.all()
    # search for query in headline, sub headline, body
    articles = Article.articlemanager.filter(
        Q(headline__icontains=query) |
        Q(sub_headline__icontains=query) |
        Q(body__icontains=query)
    )

    tags = Tag.objects.all()

    context = {
        'articles': articles,
        'tags': tags,
    }

    return render(request, 'articles.html', context)
    # return render(request,'login.html')

@login_required
def article(request, article):

    article = get_object_or_404(Article, slug=article, status='published')

    context = {
        'article': article
    }

    return render(request, 'article.html', context)

# tenant/views.py



def dashboard(request):
    return render(request, 'tenant/dashboard.html', {'tenant': request.tenant})


def login1(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f" Hello {username}, You Are Successfully Logged In")
            hostname_without_port = remove_www(request.get_host().split(':')[0])
            domain = Domain.objects.get(domain=hostname_without_port)
            name = domain.tenant.blog_name

    # feature articles on the home page
            featured = Article.articlemanager.filter(featured=True)[0:3]

            context = {
        'name':name,
        'articles': featured
    }
            return render(request, 'index.html', context)

        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, "Username Doesn't Exist")
            else:
                messages.info(request, "Incorrect Password")
            return render(request,'login.html')

    else:  
        return render(request, "login.html")
    

def logout(request):
    auth.logout(request)
    return redirect('/')

from django import forms
from django.contrib.auth.forms import UserCreationForm

class registrationform(UserCreationForm):
    email = forms.EmailField(
        required = True,
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
def register(request):
    if request.method=='POST':
        form = registrationform(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # password1 = form.cleaned_data.get('password1')
            # user = auth.authenticate(username=username,password=password1)
            # auth.login(request, user)
            messages.info(request, f'Hello {username}, You are Successfully Registered!!') 
            hostname_without_port = remove_www(request.get_host().split(':')[0])
            domain = Domain.objects.get(domain=hostname_without_port)
            name = domain.tenant.blog_name

    # feature articles on the home page
            featured = Article.articlemanager.filter(featured=True)[0:3]

            context = {
        'name':name,
        'articles': featured
    }
            return render(request, 'index.html', context)
            form = registrationform()
    else:
        form = registrationform()
    return render(request, 'register.html', {'form':form})


from django import forms
from tenant.models import Tenant


from django.contrib.auth.models import User  # Import the User model

class TenantCreationForm(forms.ModelForm):
    # Add a user field to the form
    username = forms.CharField(max_length=30, label='Desired Username')
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    class Meta:
        model = Tenant
        fields = ['username', 'email', 'password', 'blog_name', 'blog_image', 'featured', 'description', 'is_active']



# views.py
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_tenants.utils import schema_context
from tenant.models import Tenant,Domain
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.hashers import make_password


# views.py
from django.shortcuts import render, redirect
from django_tenants.utils import schema_context  # Import the Tenant model

# def create_tenant(request):
#     if request.method == 'POST':
#         form = TenantCreationForm(request.POST)
#         if form.is_valid():
#             tenant = form.save(commit=False)
#             tenant.schema_name = 'tenant' + str(Tenant.objects.count() + 1)  # Generate a unique schema name
#             tenant.save()

#             # Create and associate domain using the provided username
#             username = form.cleaned_data.get('user').username
#             domain = tenant.domains.create(domain=f'{username}.localhost', is_primary=True)
            
#             return redirect('tenant_created_success')  # Redirect to a success page
#     else:
#         form = TenantCreationForm()

#     return render(request, 'create_tenant.html', {'form': form})




# def create_tenant(request):
#     if request.method == 'POST':
#         form = TenantCreationForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
            
#             tenant = form.save(commit=False)
#             tenant.schema_name = f'{username}'
#             tenant.save()

#             # Create and associate domain using the provided username
#             domain = tenant.domains.create(domain=f'{username}.localhost', is_primary=True)
            
#             # Create superuser for the tenant
#             user = User.objects.create_user(username=username, email=email, password=password)
#             user.is_superuser = True
#             user.is_staff = True
#             user.save()
            
#             # Redirect to the subdomain URL
#             return redirect(f'http://{username}.localhost:8000')
#     else:
#         form = TenantCreationForm()

#     return render(request, 'create_tenant.html', {'form': form})



def create_tenant(request):
    if request.method == 'POST':
        form = TenantCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            tenant = form.save(commit=False)
            tenant.schema_name = f'{username}'
            tenant.save()

            # Create and associate domain using the provided username
            domain = tenant.domains.create(domain=f'{username}.localhost', is_primary=True)
            
            # Redirect to the subdomain URL
            subdomain_url = f'http://{username}.localhost:8000'
            
            # Create superuser for the tenant
            with schema_context(username):
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_superuser = True
                user.is_staff = True
                user.save()
            
            return redirect(subdomain_url)
    else:
        form = TenantCreationForm()

    return render(request, 'create_tenant.html', {'form': form})
