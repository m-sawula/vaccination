from django.shortcuts import render
from django.views import View

from django.views.generic import CreateView

from vax.models import Parent, Child

class ParentIndexView(View):
    def get(self, request, parent_id):
        parent = Parent.objects.get(id=parent_id)
        childrens = Child.objects.filter(parent=parent_id)
        return render(
            request,
            'parent/index.html',
            {
                'parent': parent,
                'childrens': childrens
            }
        )

class ParentCreateView(CreateView):
    model = Parent
    fields = ['name', 'surname', 'email']
    template_name = 'parent/parent_create.html'

