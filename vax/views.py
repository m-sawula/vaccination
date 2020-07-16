from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from vax.models import Parent, Child, ChildHealthReview, VaxProgram, VaxCycle, Vax

from django.views.generic import CreateView, UpdateView

from vax.forms.standard_forms import LoginForm, SignUpForm


class MainIndexView(View):
    """Wyświtla główna strone aplikacji po wejści na myvax"""

    def get(self, request):
        return render(request, 'main_index.html')


# logowanie do panelu, oddzielny wdok z pominięciem wbudowanego widoku django
class LoginView(View):
    def get(self, request):
        # jeżeli user.id nie jest None przekieruj na stronę główną palikacji
        if request.user.id is not None:
            return redirect('test')
        # w innym przypadku wyświetl formularz logowania
        return render(
            request,
            "auth/login.html",
            # formlarz z pliku standard_forms.py
            {"form": LoginForm()}
        )

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "auth/login.html",
                {"form": form}
            )
        # funkcja authenticate() sprawdza czy dane pobrane z forma znajdują się w bazie danych
        user = authenticate(
            request=request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )  # fetch user object

        if user is None:
            # jeżeli user jest None wyświetl komunikat
            messages.add_message(request, messages.WARNING, 'User does not exist in database!')
            # przekieruj na stronę logowania
            return redirect('myvax')
        # w innym przypadku utwórz sesje dla user
        login(request, user)  # session file aclass MainIndexView(View):nd cookie
        # wyświetl wiadomość
        messages.add_message(request, messages.SUCCESS, 'User logged in successfully')
        # przekieruj na stronę
        return redirect('test')

@login_required
def logout_view(request):
    logout(request)
    return redirect('myvax')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})

# testowa strona dla ZALOGOWANYCH
class TestIndexView(View):
    def get(self, request):
        return render(request, "test_index.html")

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


class VaxUpdateView(UpdateView):
    pass
#     model = Vax
#     fields = ['vax_date', 'symptom_after_vax']
#     template_name = 'vax/vax_update.html'
#     success_url = reverse_lazy('child-index/{child_id}')
