from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from django.views import View

from vax.models import User, Parent, Child, ChildHealthReview, VaxProgram, VaxCycle, Vax

from vax.forms.standard_forms import LoginForm, SignUpForm

from vax.forms.model_forms import ParentForm, ChildForm, VaxForm, HealthReviewForm


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


class ParentIndexView(LoginRequiredMixin, View):
    """Widok początkowy dla rodzica.

    Umożliwia edytowanie danych rodzica oraz przejście do listy dzieci.
    """
    def get(self, request):
        return render(request, "parent/parent_index.html")


class ParentPanelView(LoginRequiredMixin, View):
    """Wyświetla rodzica oraz dzieci które zarejestrował.

    Parent jest obiektem, który jest tworzony automatycznie
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
        # przekierowuje na stronę główną zalogowanego użytkownika
        return redirect('parent-index')


class ChildIndexView(LoginRequiredMixin, View):
    """Wyświetal dane dziecka, bilans zdrowia, infor o szczepieniach"""

    def get(self, request, child_id):
        child = Child.objects.get(id=child_id)
        parent = request.user.id

        child_health_reviews = ChildHealthReview.objects.filter(child_id=child_id)

        vax_program = VaxProgram.objects.filter(child=child_id)
        vax_cycles = VaxCycle.objects.filter(program__child_id=child_id)
        vaxes = Vax.objects.filter(vaxcycle__program__child_id=child_id)

        vc_gru = vax_cycles.filter(name__vax_cycle_name__icontains='gru')
        v_gru = vaxes.filter(name__vax_name__icontains='gru').order_by('exp_vax_date')

        vc_wzw = vax_cycles.filter(name__vax_cycle_name__icontains='wzw')
        v_wzw = vaxes.filter(name__vax_name__icontains='wzw').order_by('exp_vax_date')

        vc_dtp = vax_cycles.filter(name__vax_cycle_name__icontains='dtp')
        v_dtp = vaxes.filter(name__vax_name__icontains='dtp').order_by('exp_vax_date')

        vc_ipv = vax_cycles.filter(name__vax_cycle_name__icontains='ipv')
        v_ipv = vaxes.filter(name__vax_name__icontains='ipv').order_by('exp_vax_date')

        vc_hib = vax_cycles.filter(name__vax_cycle_name__icontains='hib')
        v_hib = vaxes.filter(name__vax_name__icontains='hib').order_by('exp_vax_date')

        vc_mmr = vax_cycles.filter(name__vax_cycle_name__icontains='mmr')
        v_mmr = vaxes.filter(name__vax_name__icontains='mmr').order_by('exp_vax_date')

        return render(
            request,
            'child/child_index.html',
            {
                'parent': parent,
                'child': child,

                'health_rev': child_health_reviews,

                'vax_program': vax_program,

                'vc_gru': vc_gru,
                'v_gru': v_gru,

                'vc_wzw': vc_wzw,
                'v_wzw': v_wzw,

                'vc_dtp': vc_dtp,
                'v_dtp': v_dtp,

                'vc_ipv': vc_ipv,
                'v_ipv': v_ipv,

                'vc_hib': vc_hib,
                'v_hib': v_hib,

                'vc_mmr': vc_mmr,
                'v_mmr': v_mmr,

            }
        )

class HealthReviewUpdateView(LoginRequiredMixin, View):
    def get(self, request, child_id, health_rev_id):
        child = Child.objects.get(id=child_id)
        health_rev = ChildHealthReview.objects.get(id=health_rev_id)
        form = HealthReviewForm(instance=health_rev)
        return render(request,
                      'child/child_health_rev_update.html', {
                          "form": form,
                          "health_rev": health_rev
                      }
                      )

    def post(self, request, child_id, health_rev_id):
        child = Child.objects.get(id=child_id)
        health_rev = ChildHealthReview.objects.get(id=health_rev_id)
        form = HealthReviewForm(request.POST, instance=health_rev)
        if not form.is_valid():
            return render(request,
                          'child/child_health_rev_update.html', {
                              "form": form,
                              "health_rev": health_rev
                          }
                          )
        health_rev.workup_day = form.cleaned_data['workup_day']
        health_rev.remarks = form.cleaned_data['remarks']
        health_rev.save()

        return redirect('child-index', child_id)


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
        # obiekt Child jest tworzony za pomocą napisanej metody
        # create_child, która jest w klasie ChildManager w  models.py
        Child.objects.create_child(
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


class VaxUpdateView(LoginRequiredMixin, View):
    def get(self, request, child_id, vax_id):
        child = Child.objects.get(id=child_id)
        vax = Vax.objects.get(id=vax_id)
        form = VaxForm(instance=vax)
        return render(request,
                      'vax/vax_update.html', {
                          "form": form,
                          "vax": vax
                      }
                      )

    def post(self, request, child_id, vax_id):
        # child = Child.objects.get(id=child_id)
        vax = Vax.objects.get(id=vax_id)
        form = VaxForm(request.POST, instance=vax)
        if not form.is_valid():
            return render(request,
                          'vax/vax_update.html', {
                              "form": form,
                              "vax": vax
                          }
                          )

        vax.vax_date = form.cleaned_data['vax_date']
        vax.symptom_after_vax = form.cleaned_data['symptom_after_vax']
        vax.save()
        # przekierowuje na stronę parent-panel zalogowanego użytkownika
        return redirect('child-index', child_id)