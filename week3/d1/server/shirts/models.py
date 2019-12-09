from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import bcrypt


class UserManager(models.Manager):
    def is_reg_valid(self, request):

        if len(request.POST['first_name']) < 2:
            messages.error(
                request, 'First name must be at least 2 characters.')

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
        return len(error_messages) == 0

    def login(self, request):
        # .filter ALWAYS returns a query set LIST 0 or more items
        # (need to index list)

        logged_in_user = None
        found_users = User.objects.filter(email=request.POST['email'])

        if len(found_users) > 0:
            user_from_db = found_users[0]

            is_pw_correct = bcrypt.checkpw(
                request.POST['password'].encode(),
                user_from_db.password.encode())

            if is_pw_correct:
                request.session['uid'] = user_from_db.id
                logged_in_user = user_from_db
            else:
                print('password incorrect')
        else:
            print('no user found')

        messages.error(request, 'Invalid credentials')
        return logged_in_user


class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    # this returned string is what will be shown when printing this user
    def __str__(self):
        s = '\n'
        s += f"first_name: {self.first_name}\n"
        s += f"last_name: {self.last_name}\n"
        s += f"email: {self.email}\n"
        return s


class Shirt(models.Model):
    phrase = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # model relationships
    uploaded_by = models.ForeignKey(
        'User', related_name='uploaded_shirts', on_delete=models.CASCADE)
    users_who_liked = models.ManyToManyField(
        'User', related_name='liked_shirts')

    # this returned string is what will be shown when printing this user
    def __str__(self):
        s = '\n'
        s += f"phrase: {self.phrase}\n"
        s += f"price: {self.price}\n"
        return s
