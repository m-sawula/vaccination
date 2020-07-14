from django.shortcuts import render
from django.views import View

from django.views.generic import CreateView

from vax.models import Parent, Child, ChildHealthReview, VaxProgram, VaxCycle, Vax

class MainIndexView(View):
    """Wyświtla główna strone aplikacji po wejści na myvax"""
    def get(self, request):
        return render(request, 'main_index.html')

class ParentIndexView(View):
    """Wyświetla rodzica oraz dzieci które zarejestrował"""
    def get(self, request, parent_id):
        parent = Parent.objects.get(id=parent_id)
        children = Child.objects.filter(parent=parent_id)

        return render(
            request,
            'parent/parent_index.html',
            {
                'parent': parent,
                'children': children
            }
        )

class ParentCreateView(CreateView):
    """Dodaje rodzica"""
    model = Parent
    fields = ['name', 'surname', 'email']
    template_name = 'parent/parent_create.html'

class ChildIndexView(View):
    """Wyświetal dane dziecka, bilans zdrowia, infor o szczepieniach"""
    def get(self, request, child_id):
        child = Child.objects.get(id=child_id)
        # health_review = ChildHealthReview.objects.filter(child=child_id)
        vax_program = VaxProgram.objects.filter(child=child_id)
        vax_cycles = VaxCycle.objects.filter(program__child_id=child_id)
        vaxes = Vax.objects.filter(vaxcycle__program__child_id=child_id).order_by('exp_vax_date')

        return render(
            request,
            'child/child_index.html',
            {
                'child': child,
                # 'health-review': health_review,
                'vax_program': vax_program,
                'vax_cycles': vax_cycles,
                'vaxes': vaxes
            }
        )


