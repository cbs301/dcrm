from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Customer
from .forms import CustomerForm


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'landing.html', {})
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'first_name')
    direction = request.GET.get('dir', 'asc')

    valid_sorts = ['first_name', 'last_name', 'email', 'phone', 'city', 'state', 'created_at']
    if sort not in valid_sorts:
        sort = 'first_name'
    if direction not in ['asc', 'desc']:
        direction = 'asc'

    customers = Customer.objects.all()
    if query:
        customers = customers.filter(
            first_name__icontains=query
        ) | customers.filter(
            last_name__icontains=query
        ) | customers.filter(
            email__icontains=query
        ) | customers.filter(
            phone__icontains=query
        ) | customers.filter(
            city__icontains=query
        ) | customers.filter(
            state__icontains=query
        )

    order_field = f'-{sort}' if direction == 'desc' else sort
    customers = customers.order_by(order_field)

    paginator = Paginator(customers, 25)
    page = request.GET.get('page')
    customers = paginator.get_page(page)
    columns = [
        ('first_name', 'Name'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('city', 'City'),
        ('state', 'State'),
        ('created_at', 'Created'),
    ]
    return render(request, 'home.html', {
        'customers': customers,
        'query': query,
        'sort': sort,
        'dir': direction,
        'columns': columns,
    })


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html', {})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customer_detail.html', {'customer': customer})


@login_required
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=customer)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Customer updated successfully.')
        return redirect('customer_detail', pk=pk)
    return render(request, 'edit_customer.html', {'form': form, 'customer': customer})


@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted.')
        return redirect('home')
    return render(request, 'delete_customer.html', {'customer': customer})


@login_required
def add_customer(request):
    form = CustomerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Customer added successfully.')
        return redirect('home')
    return render(request, 'add_customer.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        login(request, user)
        messages.success(request, f'Account created! Welcome, {user.username}.')
        return redirect('home')

    return render(request, 'register.html', {'form': form})
