from django.contrib import admin

from vax.models import VaxName, VaxCycleName

from vax.models import VaxProgram, VaxCycle, Vax

@admin.register(VaxName)
class VaxName(admin.ModelAdmin):
    pass

@admin.register(VaxCycleName)
class VaxCycleName(admin.ModelAdmin):
    pass

@admin.register(VaxProgram)
class VaxProgram(admin.ModelAdmin):
    list_display = ('vax_program_name', 'year', 'child')

@admin.register(VaxCycle)
class VaxCycle(admin.ModelAdmin):
    # tu wpisujemy pola z modelu, które chcemy wyświetlać w adminie
    list_display = ('name', 'program')

@admin.register(Vax)
class Vax(admin.ModelAdmin):
    list_display = (
        'name',
        'exp_vax_date',
        'vax_date',
        'symptom_after_vax',
        'vaxcycle'
    )
    # tu wpisuemy pola które, będą zablokowane do edycji w adminie
    exclude = ['exp_vax_date']

# Register your models here.
