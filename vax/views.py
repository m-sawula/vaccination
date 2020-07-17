from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from vax.models import User, Parent, Child, ChildHealthReview, VaxProgram, VaxCycle, Vax

from django.views.generic import CreateView, UpdateView

from vax.forms.standard_forms import LoginForm, SignUpForm, ChildForm
from vax.forms.model_forms import ParentForm


class MainIndexView(View):
    """Wyświtla główna strone aplikacji po wejści na myvax"""

    def get(self, request):
        return render(request, 'main_index.html')


# logowanie do panelu, oddzielny wdok z pominięciem wbudowanego widoku django
class LoginView(View):
    def get(self, request):
        # poniższy kod sprawdza czy koś jest aktualnie zlogowany
        # jeżeli request.user.id (id aktualnie zalogowanego użytkownika) nie jest None
        if request.user.id is not None:
            return redirect('parent-index')
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
            # przekieruj na stronę główną aplikacji
            return redirect('myvax')
        # w innym przypadku utwórz sesje dla user
        login(request, user)  # session file aclass MainIndexView(View):nd cookie
        # wyświetl wiadomość
        messages.add_message(request, messages.SUCCESS, 'User logged in successfully')
        # przekieruj na stronę
        return redirect('parent-index')


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
            messages.add_message(request, messages.SUCCESS, 'User created successfully')
            return redirect('parent-index')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', {'form': form})


# testowa strona dla ZALOGOWANYCH
class ParentIndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "parent/parent_index.html")


class ParentPanelView(LoginRequiredMixin, View):
    """Wyświetla rodzica oraz dzieci które zarejestrował.

    Parent jest obiektem który jest tworzony automatycznie
    podczas rejestrancj użytkownika. Po zarejestrowaniu rodzic
    musi zaktualizować swoje imie i nazwisko.
    """

    def get(self, request, user_id):
        parent = Parent.objects.get(pk=user_id)
        children = Child.objects.filter(parent_id=user_id)

        return render(
            request,
            'parent/parent_panel.html',
            {
                'parent': parent,
                'children': children
            }
        )


# class ParentUpdateView(LoginRequiredMixin, UpdateView):
#     """Ktualizuje dane rodzica stwordzonego automatycznie podczas twordzenia urzytkowniak rodzica"""
#     model = Parent
#     fields = ['first_name', 'last_name']
#     template_name = 'parent/parent_update.html'
#     success_url = reverse_lazy('parent-panel/{user_id}')

class ParentUpdateView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        # user = request.user
        parent = Parent.objects.get(user_id=user_id)
        form = ParentForm(instance=parent)
        return render(request,
                      'parent/parent_update.html', {
                          "form": form,
                          "parent": parent
                      }
                      )

    def post(self, request, user_id):
        parent = Parent.objects.get(user_id=user_id)
        form = ParentForm(request.POST, instance=parent)
        if not form.is_valid():
            return render(request,
                          'parent/parent_update.html', {
                              "form": form,
                              "parent": parent
                          }
                          )

        parent.first_name = form.cleaned_data['first_name']
        parent.last_name = form.cleaned_data['last_name']
        parent.save()
        # przekierowuje na stronę parent panel zalogowanego użytkownika
        return redirect('parent-panel', user_id)


class ChildIndexView(LoginRequiredMixin, View):
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


class ChildCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ChildForm
        return render(
            request,
            "child/child_create.html",
            {"form": form}
        )

    def post(self, request):
        form = ChildForm(request.POST)
        # Parent jest OneToOneField do User
        # tu pobierany jest rodzic który ma user_id=id aktualnie
        # zalogowanego User-a
        parent = Parent.objects.get(user_id=request.user.id)
        if not form.is_valid():
            return render(
                request,
                "child/child_create.html",
                {"form": form}
            )
        Child.objects.create(
            name=form.cleaned_data['name'],
            surname=form.cleaned_data['surname'],
            date_of_birth=form.cleaned_data['date_of_birth'],
            parent=parent.id
        )
        return redirect('parent-index')


class VaxUpdateView(LoginRequiredMixin, UpdateView):
    pass
#     model = Vax
#     fields = ['vax_date', 'symptom_after_vax']
#     template_name = 'vax/vax_update.html'
#     success_url = reverse_lazy('child-index/{child_id}')
