from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View

from vax.models import User, Parent, Child, ChildHealthReview, VaxProgram, VaxCycle, Vax

from django.views.generic import CreateView, UpdateView

from vax.forms.standard_forms import LoginForm, SignUpForm
from vax.forms.model_forms import ParentForm, ChildForm


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
            return redirect('child-index')
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
        children = Child.objects.filter(parent_id=user_id).order_by('date_of_birth')

        return render(
            request,
            'parent/parent_panel.html',
            {
                'parent': parent,
                'children': children
            }
        )


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
        # przekierowuje na stronę child panel zalogowanego użytkownika
        return redirect('parent-panel', user_id)


class ChildIndexView(LoginRequiredMixin, View):
    """Wyświetal dane dziecka, bilans zdrowia, infor o szczepieniach"""

    def get(self, request, child_id):
        child = Child.objects.get(id=child_id)
        parent = request.user.id
        # health_review = ChildHealthReview.objects.filter(child=child_id)
        vax_program = VaxProgram.objects.filter(child=child_id)
        vax_cycles = VaxCycle.objects.filter(program__child_id=child_id)
        vaxes = Vax.objects.filter(vaxcycle__program__child_id=child_id)

        vc_gru = vax_cycles.filter(name__vax_cycle_name__icontains='gru')
        v_gru = vaxes.filter(name__vax_name__icontains='gru').order_by('exp_vax_date')

        vc_wzw = vax_cycles.filter(name__vax_cycle_name__icontains='wzw')
        v_wzw = vaxes.filter(name__vax_name__icontains='wzw').order_by('exp_vax_date')

        vc_dtp = vax_cycles.filter(name__vax_cycle_name__icontains='dtp')
        v_dtp = vaxes.filter(name__vax_name__icontains='dtp').order_by('exp_vax_date')

        return render(
            request,
            'child/child_index.html',
            {
                'parent': parent,
                'child': child,
                # 'health-review': health_review,

                'vax_program': vax_program,

                'vc_gru': vc_gru,
                'v_gru': v_gru,

                'vc_wzw': vc_wzw,
                'v_wzw': v_wzw,

                'vc_dtp': vc_dtp,
                'v_dtp': v_dtp
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
        if not form.is_valid():
            return render(
                request,
                "child/child_create.html",
                {"form": form}
            )

        Child.objects.create(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            date_of_birth=form.cleaned_data['date_of_birth'],
            sex=form.cleaned_data['sex'],
            # Child.parent_id = Parent.user_id
            parent_id=request.user.id
        )
        return redirect('parent-panel', request.user.id)


class ChildUpdateView(LoginRequiredMixin, View):
    def get(self, request, child_id):
        child = Child.objects.get(id=child_id)
        form = ChildForm(instance=child)
        return render(request,
                      'child/child_update.html', {
                          "form": form,
                          "child": child
                      }
                      )

    def post(self, request, child_id):
        child = Child.objects.get(id=child_id)
        form = ChildForm(request.POST, instance=child)
        if not form.is_valid():
            return render(request,
                          'child/child_update.html', {
                              "form": form,
                              "child": child
                          }
                          )

        child.first_name = form.cleaned_data['first_name']
        child.last_name = form.cleaned_data['last_name']
        child.sex = form.cleaned_data['sex']
        child.date_of_birth = form.cleaned_data['date_of_birth']
        child.save()
        # przekierowuje na stronę parent-panel zalogowanego użytkownika
        return redirect('parent-panel', request.user.id)


class ChildDeleteViev(LoginRequiredMixin, View):
    def get(self, request, child_id):
        parent = request.user.id
        child = Child.objects.get(id=child_id)
        return render(request, 'child/child_delete.html', {"child": child, "parent": parent})

    def post(self, request, child_id):
        child = Child.objects.get(id=child_id)
        child.delete()
        messages.add_message(request, messages.SUCCESS, 'Dane dziecka zostały usunięte z bazy')
        return redirect('parent-panel', request.user.id)

class VaxUpdateView(LoginRequiredMixin, UpdateView):
    pass
