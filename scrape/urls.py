from django.urls import path
from .views import scrape

app_name = 'users'

urlpatterns = [
    path('jobs_from_other_website/', scrape, name="scrape"),
]
