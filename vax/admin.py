from django.contrib import admin

from vax.models import VaxName, VaxCycleName, VaxProgramName

from vax.models import VaxProgram, VaxCycle, Vax


@admin.register(VaxName)
class VaxName(admin.ModelAdmin):
    pass


@admin.register(VaxCycleName)
class VaxCycleName(admin.ModelAdmin):
    pass


@admin.register(VaxProgramName)
class VaxProgramName(admin.ModelAdmin):
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
        'vaxcycle',
        'exp_vax_date',
        # 'vax_date',
        # 'symptom_after_vax',
    )

    # tu wpisuemy pola które, nie będą widoczne w adminie
    # exclude = ['exp_vax_date']
