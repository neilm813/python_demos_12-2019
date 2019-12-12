from django.db import models
import re  # regex
from django.contrib import messages
from django.contrib.messages import get_messages

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def is_reg_valid(self, request):
        if len(request.POST['first_name']) < 2:
            messages.error(
                request, 'First name must be at least 2 characters.')

        if len(request.POST['last_name']) < 2:
            messages.error(request, 'Last name must be at least 2 characters.')

        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request, "Invalid email address.")

        if len(request.POST['password']) < 8:
            messages.error(request, 'Password must be at least 8 characters.')

        if request.POST['password'] != request.POST['password_confirm']:
            messages.error(request, 'Passwords must match.')

        error_messages = messages.get_messages(request)
        # don't clear messages due to them being accessed
        error_messages.used = False
        return len(error_messages) == 0


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


class DoggoManager(models.Manager):
    def is_form_valid(self, request):

        if len(request.POST['profile_pic_url']) < 1:
            messages.error(request, 'Profile picture is required.')

        if len(request.POST['bio']) < 10:
            messages.error(request, 'Bio must be at least 10 characters.')

        if len(request.POST['name']) < 2:
            messages.error(request, 'Name must be at least 2 characters.')

        error_messages = messages.get_messages(request)
        # don't clear messages due to them being accessed
        error_messages.used = False
        return len(error_messages) == 0


class Doggo(models.Model):
    name = models.CharField(max_length=60)
    profile_pic_url = models.TextField()
    bio = models.TextField()
    age = models.IntegerField()
    weight = models.IntegerField()
    is_good_boy = models.BooleanField(default=False)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DoggoManager()
    # Relationships
    submitted_by = models.ForeignKey(
        'User', on_delete='CASCADE', related_name='dogs')
    tricks = models.ManyToManyField('Trick', related_name='dogs_with_trick')

    def __str__(self):
        s = '\n'
        s += f"name: {self.name}\n"
        return s


class Trick(models.Model):
    name = models.CharField(max_length=60)
