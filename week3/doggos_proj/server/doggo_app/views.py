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
            'logged_in_user': User.objects.get(id=uid),
            'all_doggos': Doggo.objects.all()
        }
        return render(request, 'home.html', context)


def logout(request):
    request.session.clear()
    return redirect('/')


# Doggos
def doggo_new(request):

    if request.session.get('uid') is None:
        return redirect('/')
    else:

        context = {
            'tricks': Trick.objects.all(),
        }

        return render(request, 'doggos/new.html', context)


def doggo_create(request):

    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    if Doggo.objects.is_form_valid(request) is False:
        return redirect('/doggos/new')

    logged_in_user = User.objects.get(id=uid)

    new_doggo = Doggo.objects.create(
        name=request.POST['name'],
        age=request.POST['age'],
        weight=request.POST['weight'],
        bio=request.POST['bio'],
        profile_pic_url=request.POST['profile_pic_url'],
        submitted_by=logged_in_user,
        birthday=request.POST['birthday']
    )

    # Value None and value empty string will not pass an if conditon
    form_tricks = [
        # None or the value of input if checked
        request.POST.get('trick_roll_over'),
        request.POST.get('trick_sit'),
        request.POST.get('trick_shake'),

        # empty string or the value
        request.POST.get('trick_other'),
    ]

    for trick in form_tricks:
        # trick isn't None and isn't empty string
        if trick:
            found_tricks = Trick.objects.filter(name=trick)

            if len(found_tricks) > 0:
                trick_from_db = found_tricks[0]
                new_doggo.tricks.add(trick_from_db)

            # trick not in db, create it
            else:
                new_trick = Trick.objects.create(name=trick)
                new_doggo.tricks.add(new_trick)

    return redirect(f'/doggos/{new_doggo.id}')


def doggo_profile(request, doggo_id):

    if request.session.get('uid') is None:
        return redirect('/')
    else:
        found_doggos = Doggo.objects.filter(id=doggo_id)

        if len(found_doggos) == 0:
            # no doggo found, bad id
            return redirect('/home')
        else:
            context = {
                'doggo': found_doggos[0]
            }
            return render(request, 'doggos/profile.html', context)


def doggos(request):

    if request.session.get('uid') is None:
        return redirect('/')

    else:
        context = {
            'good_boys': Doggo.objects.filter(is_good_boy=True),
            'bad_boys': Doggo.objects.filter(is_good_boy=False),
        }

        return render(request, 'doggos/all.html', context)


def doggo_toggle_good_boy(request, doggo_id):

    if request.session.get('uid') is None:
        return redirect('/')

    found_doggos = Doggo.objects.filter(id=doggo_id)

    if len(found_doggos) != 0:
        # since doggos list is not empty, there should be 1 doggo
        # extract the single doggo from the list
        doggo = found_doggos[0]
        doggo.is_good_boy = not doggo.is_good_boy
        doggo.save()

    return redirect('/doggos')


def doggo_delete(request, doggo_id):

    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    logged_in_user = User.objects.get(id=uid)

    found_doggos = Doggo.objects.filter(id=doggo_id)

    if len(found_doggos) > 0:
        doggo_to_delete = found_doggos[0]

        if logged_in_user == doggo_to_delete.submitted_by:
            doggo_to_delete.delete()

    return redirect('/doggos')


def doggo_edit(request, doggo_id):

    if request.session.get('uid') is None:
        return redirect('/')

    found_doggos = Doggo.objects.filter(id=doggo_id)

    if len(found_doggos) > 0:
        doggo_to_edit = found_doggos[0]

        context = {
            'doggo_to_edit': doggo_to_edit,
            'formatted_birthday': doggo_to_edit.birthday.strftime("%Y-%m-%d")
        }

        return render(request, 'doggos/edit.html', context)
    else:
        return redirect('/doggos/all')


def doggo_update(request, doggo_id):

    uid = request.session.get('uid')

    if uid is None:
        return redirect('/')

    if Doggo.objects.is_form_valid(request) is False:
        return redirect(f'/doggos/{doggo_id}/edit')

    found_doggos = Doggo.objects.filter(id=doggo_id)

    if len(found_doggos) > 0:

        logged_in_user = User.objects.get(id=uid)
        doggo_to_update = found_doggos[0]

        if logged_in_user != doggo_to_update.submitted_by:
            # return to prevent updating
            return redirect('/doggos')

        doggo_to_update.name = request.POST['name']
        doggo_to_update.profile_pic_url = request.POST['profile_pic_url']
        doggo_to_update.bio = request.POST['bio']
        doggo_to_update.age = request.POST['age']
        doggo_to_update.weight = request.POST['weight']
        doggo_to_update.tricks = request.POST['tricks']
        doggo_to_update.birthday = request.POST['birthday']
        doggo_to_update.save()
        return redirect(f'/doggos/{doggo_id}')
    # no dog found
    else:
        return redirect('/home')
