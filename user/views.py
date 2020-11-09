from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from .forms import CreateUserForm
from chat.models import Student, Teacher, Chat
from .decorators import unauthenticated_user, allowed_users

@unauthenticated_user
def signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            profession = form.cleaned_data['profession']
            if profession=='student':
                group = Group.objects.get(name=profession)
                user.groups.add(group)
                Student.objects.create(
                        user = user,
                        name = user.first_name + ' ' +user.last_name
                    )
            else:
                group = Group.objects.get(name=profession)
                user.groups.add(group)
                Teacher.objects.create(
                        user = user,
                        name = user.first_name + ' ' +user.last_name
                    )
            return redirect('signin')
    context = {
        'form': form
    }
    return render(request, 'signup.html', context)

@unauthenticated_user
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    context = {}
    return render(request, 'signin.html', context)

@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
@allowed_users(allowed_roles=['student', 'teacher'])
def index(request):
    user = request.user
    group = str(request.user.groups.all()[0])
    lst = []
    if group=='student':
        lst = Teacher.objects.all()
    else:
        lst = Student.objects.all()

    print(len(lst))
    context = {
        'profession': group,
        'lst': lst
    }
    return render(request, 'index.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['student', 'teacher'])
def startchatWithTeacher(request, id):
    student = Student.objects.get(user=request.user)
    teacher = Teacher.objects.get(id=int(id))
    chat = Chat.objects.get_or_create(student=student, teacher=teacher)[0]
    data = chat.data
    slugurl = chat.slug
    return redirect(f'../../chat/{slugurl}')

@login_required(login_url='signin')
@allowed_users(allowed_roles=['student', 'teacher'])
def startchatWithStudent(request, id):
    teacher = Teacher.objects.get(user=request.user)
    student = Student.objects.get(id=int(id))
    chat = Chat.objects.get_or_create(student=student, teacher=teacher)[0]
    data = chat.data
    slugurl = chat.slug
    return redirect(f'../../chat/{slugurl}')