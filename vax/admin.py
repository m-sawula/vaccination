from django.contrib import admin

from vax.models import VaxName, VaxCycleName, VaxProgramName

from vax.models import VaxProgram, VaxCycle, Vax


@admin.register(VaxName)
class VaxName(admin.ModelAdmin):
    ordering = ('vax_name',)


@admin.register(VaxCycleName)
class VaxCycleName(admin.ModelAdmin):
    ordering = ('vax_cycle_name',)


@admin.register(VaxProgramName)
class VaxProgramName(admin.ModelAdmin):
    ordering = ('vax_program_name',)


@admin.register(VaxProgram)
class VaxProgram(admin.ModelAdmin):
    list_display = ('vax_program_name', 'year', 'child')


@admin.register(VaxCycle)
class VaxCycle(admin.ModelAdmin):
    # tu wpisujemy pola z modelu, które chcemy wyświetlać w adminie
    list_display = ('name', 'program')
    ordering = ('name',)  # uwaga na przecinek nienawiści


@admin.register(Vax)
class Vax(admin.ModelAdmin):
    list_display = (
        'name',
        'vaxcycle',
        'exp_vax_date',
    )
    ordering = ('name',)  # uwaga na przecinek nienawiści
    # search_fields = ('name',)  # uwaga na przecinek nienawiści
    exclude = ['vax_date', 'symptom_after_vax']  # tu wpisuemy pola które, nie będą widoczne w adminie
