from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Student
from .forms import StudentForm


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

    students = Student.objects.all()
    if query:
        students = students.filter(
            first_name__icontains=query
        ) | students.filter(
            last_name__icontains=query
        ) | students.filter(
            email__icontains=query
        ) | students.filter(
            phone__icontains=query
        ) | students.filter(
            city__icontains=query
        ) | students.filter(
            state__icontains=query
        )

    order_field = f'-{sort}' if direction == 'desc' else sort
    students = students.order_by(order_field)

    paginator = Paginator(students, 25)
    page = request.GET.get('page')
    students = paginator.get_page(page)

    columns = [
        ('first_name', 'Name'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('city', 'City'),
        ('state', 'State'),
        ('created_at', 'Created'),
    ]
    return render(request, 'home.html', {
        'students': students,
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
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'student_detail.html', {'student': student})


@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully.')
        return redirect('student_detail', pk=pk)
    return render(request, 'edit_student.html', {'form': form, 'student': student})


@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted.')
        return redirect('home')
    return render(request, 'delete_student.html', {'student': student})


@login_required
def add_student(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Student added successfully.')
        return redirect('home')
    return render(request, 'add_student.html', {'form': form})


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
