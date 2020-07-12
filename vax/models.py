
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
    date_of_birth = models.DateField(null=True)
    sex = models.CharField(max_length=1, choices=SEX)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)


class Tuberculosis(models.Model):
    expected_vax_date_1_day = models.DateField()
    vax_date_1_day = models.DateTimeField()  # hour are crucial
    vax_name_1_day = models.CharField(max_length=64)
    symptom_after_vax_1_day = models.TextField()


class Tuberculosis2005(Tuberculosis):
    expected_vax_date_12_m = models.DateField()
    vax_date_12_m = models.DateField()
    vax_name_12_m = models.CharField(max_length=64)
    symptom_after_vax_12_m = models.TextField()

    expected_vax_date_7_y = models.DateField()
    vax_date_7_y = models.DateField()
    vax_name_7_y = models.CharField(max_length=64)
    symptom_after_vax_7_y = models.TextField()

    expected_vax_date_12_y = models.DateField()
    vax_date_12_y = models.DateField()
    vax_name_12_y = models.CharField(max_length=64)
    symptom_after_vax_12_y = models.TextField()


class HepatitisB(models.Model):
    expected_vax_date_1_day = models.DateField()
    vax_date_1_day = models.DateTimeField()  # hour are crucial
    vax_name_1_day = models.CharField(max_length=64)
    symptom_after_vax_1_day = models.TextField()

    expected_vax_date_2_m = models.DateField()
    vax_date_2_m = models.DateField()
    vax_name_2_m = models.CharField(max_length=64)
    symptom_after_vax_2_m = models.TextField()

    expected_vax_date_7_m = models.DateField()
    vax_date_7_m = models.DateField()
    vax_name_7_m = models.CharField(max_length=64)
    symptom_after_vax_7_m = models.TextField()