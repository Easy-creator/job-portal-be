from django.urls import path
from .views import ScrapeAPIView

app_name = 'users'

urlpatterns = [
    path('jobs_from_other_website/', ScrapeAPIView.as_view(), name="scrape"),
]
