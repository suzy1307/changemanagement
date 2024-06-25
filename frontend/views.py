from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render ,HttpResponse
from django.contrib.auth.decorators import login_required


from django.http import JsonResponse
from .forms import InputForm
import json


# @login_required

def index(request):
    return render(request, 'index.html')
    #return HttpResponse("This will be first page. JODDDDDDD!!!!!!!!!!!!!!!!!!!")
def about(request):
    #return HttpResponse("This will be ABOUT page. JODDDDDDD!!!!!!!!!!!!!!!!!!!")

    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            data = {
                "url": form.cleaned_data['url'],
                "credentials": {
                    "username": form.cleaned_data['username'],
                    "password": form.cleaned_data['password']
                },
                "search_term": form.cleaned_data['search_term'],
                "summary_text": form.cleaned_data['summary_text'],
                "affected_area": form.cleaned_data['affected_area'],
                "company_name": form.cleaned_data['company_name'],
                "requested_date": form.cleaned_data['requested_date'].strftime('%b %d, %Y'),
                "end_date": form.cleaned_data['end_date'].strftime('%b %d, %Y'),
                "Number_of_Users_selector_": form.cleaned_data['number_of_users'],
                "Affected_Services_selector_": form.cleaned_data['affected_services'],
                "Resources_required_to_Prepare_selector_": form.cleaned_data['resources_required'],
                "Preparation_Effort_selector_": form.cleaned_data['preparation_effort'],
                "Implementation_duration_selector_": form.cleaned_data['implementation_duration'],
                "Failure_Exposure_selector_": form.cleaned_data['failure_exposure'],
            }
            response = HttpResponse(json.dumps(data), content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="data.json"'
            return response
    else:
        form = InputForm()
    
    return render(request, 'input_form.html', {'form': form})





