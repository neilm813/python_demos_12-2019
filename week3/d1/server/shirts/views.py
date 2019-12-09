from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
import bcrypt

from .models import *


def index(request):
    # if already logged in
    if request.session.get('uid'):
        return redirect('/home')
    else:
        return render(request, 'index.html')


def login(request):
    # when added to session, user is considered 'logged in'

    # .filter ALWAYS returns a query set LIST 0 or more items
    # (need to index list)
    found_users = User.objects.filter(email=request.POST['email'])

    if len(found_users) > 0:
        user_from_db = found_users[0]

        is_pw_correct = bcrypt.checkpw(
            request.POST['password'].encode(), user_from_db.password.encode())

        if is_pw_correct:
            request.session['uid'] = user_from_db.id
            return redirect('/home')
        else:
            print('password incorrect')
    else:
        print('no user found')

    messages.error(request, 'Invalid credentials')
    return redirect('/')


def register(request):

    if len(request.POST['first_name']) < 2:
        messages.error(request, 'First name must be at least 2 characters.')

    if len(request.POST['last_name']) < 2:
        messages.error(request, 'Last name must be at least 2 characters.')

    if len(request.POST['email']) < 3:
        messages.error(request, 'Email must be at least 3 characters.')

    if len(request.POST['password']) < 8:
        messages.error(request, 'Password must be at least 8 characters.')

    if request.POST['password'] != request.POST['password_confirm']:
        messages.error(request, 'Passwords must match.')

    error_messages = messages.get_messages(request)
    # don't clear messages due to them being accessed
    error_messages.used = False

    if len(error_messages) > 0:
        return redirect('/')

    hashed_pw = bcrypt.hashpw(
        request.POST['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(first_name=request.POST['first_name'],
                                   last_name=request.POST['last_name'],
                                   email=request.POST['email'],
                                   password=hashed_pw)

    request.session['uid'] = new_user.id

    return redirect('/home')


def home(request):
    uid = request.session.get('uid')

    if uid is not None:
        user_from_db = User.objects.get(id=uid)

        context = {
            'user': user_from_db
        }
        return render(request, 'home.html', context)
    else:
        return redirect('/')


def users_profile(request, id):
    uid = request.session.get('uid')

    if uid is not None:
        user_from_db = User.objects.get(id=uid)

        context = {
            'user': user_from_db
        }
        return render(request, 'profile.html', context)
    else:
        return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')


# SHIRTS Section

def new_shirt(request):
    if request.session.get('uid') is None:
        return redirect('/')

    return render(request, 'shirts/new.html')


def create_shirt(request):
    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    logged_in_user = User.objects.get(id=uid)

    new_shirt = Shirt.objects.create(
        phrase=request.POST['phrase'],
        price=request.POST['price'],
        uploaded_by=logged_in_user)

    return redirect('/shirts')


def all_shirts(request):
    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    logged_in_user = User.objects.get(id=uid)

    context = {
        'all_shirts': Shirt.objects.all(),
        'logged_in_user': logged_in_user,
    }
    return render(request, 'shirts/all.html', context)


def like_shirt(request, shirt_id):
    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    logged_in_user = User.objects.get(id=uid)

    found_shirts = Shirt.objects.filter(id=shirt_id)

    if len(found_shirts) > 0:
        shirt_to_like = found_shirts[0]

        if logged_in_user in shirt_to_like.users_who_liked.all():
            shirt_to_like.users_who_liked.remove(logged_in_user)
        else:
            shirt_to_like.users_who_liked.add(logged_in_user)

    return redirect('/shirts')
