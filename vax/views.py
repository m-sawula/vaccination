from django.shortcuts import render
from django.views import View

from django.views.generic import CreateView

from vax.models import Parent, Child

class ParentIndexView(View):
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
    model = Parent
    fields = ['name', 'surname', 'email']
    template_name = 'parent/parent_create.html'

class ChildIndexView(View):
    pass


