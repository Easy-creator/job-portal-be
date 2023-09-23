from django.shortcuts import render
import requests
from django.http import HttpResponse

# Create your views here.
def scrape(request):
    url = "https://www.glassdoor.com/Job/index.htm"
    html = requests.get(url)
    print(html.status_code)

    return HttpResponse('success fully')