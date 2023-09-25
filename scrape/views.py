from django.shortcuts import render
import requests
from django.http import HttpResponse, JsonResponse
from bs4 import BeautifulSoup
import json
from rest_framework.response import Response


# Create your views here.
def scrape(request):
    job_lists = [] 
    
    # check the page requested 
    i = request.GET.get('page')
    if i == None:
        i=1
    print(i)

    url = f"https://www.adzuna.com/search?p={i}"
    print(url)
    response = requests.get(url)
    b = BeautifulSoup(response.content, "html.parser")
    results = b.find(class_ = 'ui-search-results')
    jobs = results.select('.ui-search-results > div') 
    
    jobs_list = []
    for job in jobs:
        logo_find = job.find('div', class_ = 'ui-logo-col')
        if logo_find:
            # getting job info
            job_link = logo_find.find('a')
            img = job_link.find('img')
            info = job.find('div', class_ = 'w-full')
            company = info.find('div', class_ = 'ui-job-card-info').find('a')
            salary = info.find('div', class_ = 'ui-salary')
            salary_to_text = ' '.join(salary.stripped_strings) if salary else 'Not available'
            job_desc = info.find('div', class_ = 'hidden sm:block md:w-auto mt-1')
            job_description = job_desc.find('span') if job_desc else 'Not available'
            
            job_title = info.find('h2').find('a')
            job_title = ' '.join(job_title.stripped_strings) if job_title else "Failed to Get title"
            link = job_link.get('href')
            company_link = company.get('href')
            company_name = company.text
            location = info.find('div', class_ = 'ui-location').text
            img_link = img.get('src')
            cleaned_salary = salary_to_text.replace('?', '')
            job_description = ' '.join(job_description.stripped_strings)

            job_data = {'title': job_title,
                        'link': link,
                        'company-link': company_link,
                        'company-name': company_name,
                        'location': location,
                        'img': img_link,
                        'salary': cleaned_salary,
                        'job_desc': job_description
                        }
            
            jobs_list.append(job_data)
    
    

    # job_lists.append(jobs_list)

                
    data = json.dumps(jobs_list, indent=2, ensure_ascii=False)

    return HttpResponse(data, content_type="application/json")
