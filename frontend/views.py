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
from frontend.forms import ExcelFileForm

# from django.views.generic.edit import FormView
# from django.urls import reverse_lazy
# from .forms import ExcelFileForm
import pandas as pd
import openpyxl
from django.conf import settings
from django.views import View
from django import forms

PROJECTS = ['PLDT', 'Maxis', 'TKS']

# @login_required



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




class ProjectSelectForm(forms.Form):
    project = forms.ChoiceField(choices=[(project, project) for project in PROJECTS], label="Select Project")

class ProjectSelectView(View):
    template_name = 'project_select.html'
    form_class = ProjectSelectForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            return redirect('fill_project_template', project_name=project)
        return render(request, self.template_name, {'form': form})
    
class FillProjectTemplateView(View):
    template_name = 'fill_project_template.html'

    def get_placeholder_fields(self, wb):
        placeholders = set()
        for sheet in wb:
            for row in sheet.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str) and '<' in cell.value and '>' in cell.value:
                        placeholders.add(cell.value.strip('<>'))
        return placeholders

    def get(self, request, project_name, *args, **kwargs):
        template_path = os.path.join(settings.BASE_DIR, 'templates', f'{project_name}.xlsx')
        wb = openpyxl.load_workbook(template_path)
        
        placeholders = self.get_placeholder_fields(wb)
        
        # Dynamically create a form class with CharField for each placeholder
        form_class = type('DynamicForm', (ExcelFileForm,), {placeholder: forms.CharField(label=placeholder) for placeholder in placeholders})
        form = form_class()
        
        return render(request, self.template_name, {'form': form, 'project_name': project_name})

    def post(self, request, project_name, *args, **kwargs):
        template_path = os.path.join(settings.BASE_DIR, 'templates', f'{project_name}.xlsx')
        wb = openpyxl.load_workbook(template_path)
        
        placeholders = self.get_placeholder_fields(wb)
        
        form_class = type('DynamicForm', (ExcelFileForm,), {placeholder: forms.CharField(label=placeholder) for placeholder in placeholders})
        form = form_class(request.POST)
        
        if form.is_valid():
            for sheet in wb:
                for row in sheet.iter_rows():
                    for cell in row:
                        if isinstance(cell.value, str) and '<' in cell.value and '>' in cell.value:
                            placeholder = cell.value.strip('<>')
                            cell.value = form.cleaned_data[placeholder]

            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{project_name}_filled.xlsx"'
            wb.save(response)
            return response

        return render(request, self.template_name, {'form': form, 'project_name': project_name})





