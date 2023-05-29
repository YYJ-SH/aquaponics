"""
URL configuration for aqua project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from backend.views import login_view
from backend.views import yolov5_detection
from backend.views import register_member
from backend.views import store_image_data
from backend.views import get_data_by_arduino_id
from backend.views import arduinopic_view
from backend.views import led_on
from backend.views import led_off
from backend.views import moter_off
from backend.views import moter_on
from backend.views import moter_once
from backend.views import dark_neo


urlpatterns = [
    path('api/login/', login_view, name='login'), 
  
    path('api/upload/', yolov5_detection, name='detect'),


    path('store_image_data/', store_image_data, name='store_image_data'),
    path('arduinopic', arduinopic_view, name='arduinopic'),
    path('api/ledon', led_on, name='led_on'),
    path('api/ledoff', led_off, name='led_off'),
    path('api/moteroff', moter_off, name='moter_off'),
    path('api/moteron', moter_on, name='moter_on'),
    path('api/moteronce', moter_once, name='moter_once'),
    path('api/darkneo', dark_neo, name='dark_neo'),

    path('register/', register_member, name='register_member'),
    path('api/getData/<str:arduino_id>/', get_data_by_arduino_id, name='get_data_by_arduino_id'),

    # Other URL patterns
]