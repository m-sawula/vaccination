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

from vax.views import MainIndexView
from vax.views import ParentIndexView, ParentCreateView
from vax.views import ChildIndexView
from vax.views import VaxUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('myvax', MainIndexView.as_view(), name='myvax'),

    path('parent/<int:parent_id>', ParentIndexView.as_view(), name='parent-index'),
    path('parent/create', ParentCreateView.as_view(), name='parent-create'),

    path('child/<int:child_id>', ChildIndexView.as_view(), name='child-index'),

    # path('child/<int:child_id>/vax_update/<int:pk>', VaxUpdateView.as_view(), name='vax-update'),

]

