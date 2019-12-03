from django.shortcuts import render, redirect


def index(request):
    # if already logged in
    if request.session.get('uid'):
        return redirect('/home')
    else:
        return render(request, 'index.html')


def login(request):
    # when added to session, user is considered 'logged in'
    request.session['uid'] = request.POST['email']
    return redirect('/home')


def register(request):
    request.session['uid'] = request.POST['email']
    print(request.POST)
    return redirect('/home')


def home(request):
    uid = request.session.get('uid')

    if uid is not None:
        return render(request, 'home.html')
    else:
        return redirect('/')


def logout(request):
    request.session.clear()
    return redirect('/')
