"""test_france URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from . import vues
from mes_models import une_ville

urlpatterns = [
    path('', vues.principale),
    path('test1/', vues.test1),
    path('test1/info/', vues.info_sur_une_ville),
    path('test2/', vues.test2),
    path('test2/validation-evenement/', vues.valider_evenement),
    # ulr de recherche auto complement
    path('rech_test/', vues.RechercheAuto.as_view()),
    path('admin/', admin.site.urls),

]
