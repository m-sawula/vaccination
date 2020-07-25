"""vaccination URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from vax.views import MainIndexView, LoginView, logout_view, signup
from vax.views import ParentIndexView, ParentPanelView, ParentUpdateView
from vax.views import ChildIndexView, ChildCreateView, ChildUpdateView, ChildDeleteViev
from vax.views import VaxUpdateView, HealthReviewUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('myvax', MainIndexView.as_view(), name='myvax'),
    # path('test/', TestIndexView.as_view(), name='test'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),


    path('parent/', ParentIndexView.as_view(), name='parent-index'),
    path('parent/panel/<int:user_id>', ParentPanelView.as_view(), name='parent-panel'),
    path('parent/update/<int:user_id>', ParentUpdateView.as_view(), name='parent-update'),

    path('child/<int:child_id>', ChildIndexView.as_view(), name='child-index'),
    path('child/create', ChildCreateView.as_view(), name='child-create'),
    path('child/update/<int:child_id>', ChildUpdateView.as_view(), name='child-update'),
    path('child/delete/<int:child_id>', ChildDeleteViev.as_view(), name='child-delete'),

    path('child/<int:child_id>/vax/<int:vax_id>/update', VaxUpdateView.as_view(), name='child-vax-update'),
    path('child/<int:child_id>/health_rev/<int:health_rev_id>/update', HealthReviewUpdateView.as_view(), name='health-rev-update'),

]

