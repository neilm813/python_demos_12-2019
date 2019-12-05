from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
