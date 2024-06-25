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
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import ExcelFileForm
import pandas as pd



# @login_required
class UploadExcelView(FormView):
    template_name = 'upload_excel.html'
    form_class = ExcelFileForm
    success_url = reverse_lazy('modify_excel')

    def form_valid(self, form):
        file = form.cleaned_data['file']
        df = pd.read_excel(file)
        self.request.session['df'] = df.to_dict()
        return super().form_valid(form)
    
#def index(request):
    #return render(request, 'index.html')
    #return HttpResponse("This will be first page. JODDDDDDD!!!!!!!!!!!!!!!!!!!")
def modify_excel(request):
    df_dict = request.session.get('df')
    if not df_dict:
        return redirect('upload_excel')
    
    if request.method == 'POST':
        modified_data = {}
        for key in df_dict.keys():
            modified_data[key] = request.POST[key]
        
        df = pd.DataFrame.from_dict(modified_data)
        # Save the modified DataFrame back to Excel or perform further operations
        # Example: df.to_excel('modified_excel.xlsx', index=False)

        return redirect('upload_excel')  # Redirect to upload page or another view
    
    context = {
        'df_dict': df_dict
    }
    return render(request, 'modify_excel.html', context)


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





