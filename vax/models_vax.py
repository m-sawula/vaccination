from django.db import models

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