from django.shortcuts import render, redirect


def index(request):
    context = {
        "people": ['Neil', 'Shaun', 'Juan']
    }
    return render(request, 'index.html', context)


def guest(request, name):
    context = {
        'guest_name': name
    }
    return render(request, 'guest.html', context)


def new(request):
    print(request.POST)
    print(request.POST['email'])
    return redirect('/')
