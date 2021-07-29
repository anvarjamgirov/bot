from django.urls import path
from bot.views import web_hook

urlpatterns = [
    path('<str:token>/', web_hook),
]
