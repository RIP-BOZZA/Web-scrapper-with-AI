from django.urls import path
from . import views


urlpatterns = [
    path('save-entity/',views.WebScrapper.as_view()),
    path('get-entity/',views.WebScrapper.as_view())
]
