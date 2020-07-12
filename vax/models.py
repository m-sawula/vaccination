from datetime import datetime

from django.db import models


class Parent(models.Model):
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
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    @property
    def age(self):
        return int(datetime.now() - self.date_of_birth)

    # expected_vax_date_7_y = models.DateField()
    # vax_date_7_y = models.DateField()
    # vax_name_7_y = models.CharField(max_length=64)
    # symptom_after_vax_7_y = models.TextField()

class ChildHealthReview(models.Model):
    NAME_CHILD_REVIEW = (
        (1, 'post-birth workup'),
        (2, 'midwife home visit on the 7th day of life'),
        (3, 'workup on the 1th month of life'),
        (4, 'midwife home visit on the 3th month of life'),
        (5, 'workup on the 6th month of life'),
        (6, 'workup on the 12th month of life'),
        (7, 'workup on the 2th year of life'),
        (8, 'workup on the 4th year of life'),
        (9, 'workup on the 6th year of life'),
        (10, 'workup on the 10th year of life'),
        (11, 'workup on the 15th year of life'),
        (12, 'workup on the 18th year of life'),

    )
    name_child_review = models.IntegerField(choices=NAME_CHILD_REVIEW, default=0)
    exp_workup_day = models.DateField()
    workup_day = models.DateField()
    remarks = models.TextField()
    child = models.ManyToManyField(Child)

#
# class VaxName(models.Model):
#     """The model stores inoculation names only."""
#     vax_name = models.CharField(max_length=64)
#
#
# class VaxCycleName(models.Model):
#     """The model stores vaccination cycle names only."""
#     vax_cycle_name = models.CharField(max_length=64)
#
#
# class VaxProgram(models.Model):
#     """The model stores vaccination program names.
#
#     One program for year.
#     """
#     vax_program_name = models.CharField(max_length=64)
#     year = models.IntegerField()
#     child = models.ForeignKey(Child, on_delete=models.CASCADE)
#
#
# class VaxCycle(models.Model):
#     """The model stores vaccination cycle names.
#
#     For example: vaccination cycle for hepatitis B in 2005 year
#     contains 3 inoculations (1th day, 2th, 7th month).
#     """
#     name = models.ForeignKey(VaxCycleName, on_delete=models.CASCADE)
#     program = models.ForeignKey(VaxProgram, on_delete=models.CASCADE)
#
#
# class Vax(models.Model):
#     """The model stores information about the inoculation procedure.."""
#     name = models.ForeignKey(VaxName, on_delete=models.CASCADE)
#     exp_vax_date = models.DateField()
#     vax_date = models.DateField(null=True)
#     symptom_after_vax = models.TextField(null=True)
#     vaxcycle = models.ForeignKey(VaxCycle, on_delete=models.CASCADE)
#
#
# """
# # tworzenie programu na dany rok
#
# vaxprogram2005 = VaxProgram.objects.create(name="progrm2005", year = 2005)
# vaxprogram2010 = VaxProgram.objects.create(name="progrm2010", year = 2010)
#
# # tworzenie cyklu dla danego rodzaju szczepienia
#
# vaxcycle_t = VaxCycle.objects.create(vax_cycle_name="Tuberculosis2005", program=vaxprogram2005)
#
# vaxcycle_h = VaxCycle.objects.create(vax_cycle_name="Hepatitis2005", program=vaxprogram2005)
#
# # tworzenie konkretnych zabiegów szczepienia
#
# vaxt1 = Vax.objects.create(
#     vax_name="Tuberculosis 1-th day",
#     exp_vax_date=child.date_of_birth + timedelta(days = 1),
#     vaxcycle=vaxcycle_t
# )
#
# vaxt2 = Vax.objects.create(
#     vax_name="Tuberculosis 12-th month",
#     exp_vax_date=child.date_of_birth + timedelta(months = 12),
#     vaxcycle=vaxcycle_t
# )
#
# vaxt3 = Vax.objects.create(
#     vax_name="Tuberculosis 7-th year",
#     exp_vax_date=child.date_of_birth + timedelta(years = 7),
#     vaxcycle=vaxcycle_t
# )
#
# vaxt4 = Vax.objects.create(
#     vax_name="Tuberculosis 12-th year",
#     exp_vax_date=child.date_of_birth + timedelta(years = 12),
#     vaxcycle=vaxcycle_t
# )
#
#
#
# """
