from django.db import models

class Parent(models. Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    create_date = models.DateTimeField(auto_now_add=True)


class Child(models.Model):
    SEX = (
        ("M", "male"),
        ("F", "female")
    )
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    date_of_birth = models.DateField
    sex = models.CharField(max_length=1, choices=SEX)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)