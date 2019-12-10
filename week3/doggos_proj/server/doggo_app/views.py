from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
import bcrypt

from .models import *


def index(request):

    # not logged in
    if request.session.get('uid') is None:
        return render(request, 'index.html')
    # already logged in
    else:
        return redirect('/home')


# @require_http_methods(["POST"])
def login(request):

    # .filter returns a list, either empty or not
    found_users = User.objects.filter(email=request.POST['email'])

    if len(found_users) < 1:
        messages.error(request, 'Invalid credentials')
        return redirect('/')
    else:
        user_from_db = found_users[0]

        is_pw_correct = bcrypt.checkpw(request.POST['password'].encode(),
                                       user_from_db.password.encode())

        if is_pw_correct is True:
            request.session['uid'] = user_from_db.id
            return redirect('/home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/')


def register(request):

    if User.objects.is_reg_valid(request) is False:
        # redirect back to same page they came from to display errors
        return redirect('/')

    else:
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(),
            bcrypt.gensalt()
        ).decode()

        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hashed_pw,
        )

        request.session['uid'] = new_user.id
        return redirect('/home')


def home(request):

    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')
    else:
        context = {
            'logged_in_user': User.objects.get(id=uid)
        }
        return render(request, 'home.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')
