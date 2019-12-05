from django.shortcuts import render, redirect
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

        if user_from_db.password == request.POST['password']:
            request.session['uid'] = user_from_db.id
            return redirect('/home')
        else:
            print('password incorrect')
    else:
        print('no user found')

    return redirect('/')


def register(request):
    # add validations later

    new_user = User.objects.create(first_name=request.POST['first_name'],
                                   last_name=request.POST['last_name'],
                                   email=request.POST['email'],
                                   password=request.POST['password'])

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
    if not request.session.get('uid'):
        return redirect('/')

    return render(request, 'shirts/new.html')


def create_shirt(request):
    uid = request.session.get('uid')

    if not uid:
        return redirect('/')

    logged_in_user = User.objects.get(id=uid)

    new_shirt = Shirt.objects.create(
        phrase=request.POST['phrase'],
        price=request.POST['price'],
        uploaded_by=logged_in_user)

    return redirect('/shirts')


def all_shirts(request):
    if not request.session.get('uid'):
        return redirect('/')

    context = {
        'all_shirts': Shirt.objects.all()
    }
    return render(request, 'shirts/all.html', context)
