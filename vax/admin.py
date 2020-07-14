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
    pass

@admin.register(VaxCycle)
class VaxCycle(admin.ModelAdmin):
    pass

@admin.register(Vax)
class Vax(admin.ModelAdmin):
    pass

# Register your models here.
