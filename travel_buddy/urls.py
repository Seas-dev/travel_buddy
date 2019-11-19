"""travel_buddy URL Configuration

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
from travel_app import views

urlpatterns = [
	path('', views.mainPage),
	path('main', views.index),
	path('logout', views.logout),
	path('validreg', views.validReg),
	path('validlog', views.validLog),
	path('dashboard', views.dashboard),
	path('addtrip', views.addTrip),
	path('validtrip', views.validTrip),
	path('jointrip', views.joinTrip),
	path('travels/destination/<id>', views.destination),
	path('admin/', admin.site.urls),
]
