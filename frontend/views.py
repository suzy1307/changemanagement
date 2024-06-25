from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import View
from django import forms
from .forms import InputForm, DynamicForm
import os
import json
import openpyxl

PROJECTS = ['PLDT', 'Maxis', 'TKS']

class AboutView(View):
    template_name = 'input_form.html'

    def get(self, request, *args, **kwargs):
        form = InputForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
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
        return render(request, self.template_name, {'form': form})

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
        try:
            wb = openpyxl.load_workbook(template_path)
        except FileNotFoundError:
            return HttpResponse(f'Template file not found: {template_path}', status=404)
        except openpyxl.utils.exceptions.InvalidFileException:
            return HttpResponse(f'Invalid template file: {template_path}', status=400)

        placeholders = self.get_placeholder_fields(wb)

        form_class = type('DynamicForm', (DynamicForm,), {placeholder: forms.CharField(label=placeholder) for placeholder in placeholders})
        form = form_class()

        return render(request, self.template_name, {'form': form, 'project_name': project_name})

    def post(self, request, project_name, *args, **kwargs):
        template_path = os.path.join(settings.BASE_DIR, 'templates', f'{project_name}.xlsx')
        try:
            wb = openpyxl.load_workbook(template_path)
        except FileNotFoundError:
            return HttpResponse(f'Template file not found: {template_path}', status=404)
        except openpyxl.utils.exceptions.InvalidFileException:
            return HttpResponse(f'Invalid template file: {template_path}', status=400)

        placeholders = self.get_placeholder_fields(wb)

        form_class = type('DynamicForm', (DynamicForm,), {placeholder: forms.CharField(label=placeholder) for placeholder in placeholders})
        form = form_class(request.POST)

        if form.is_valid():
            try:
                for sheet in wb:
                    for row in sheet.iter_rows():
                        for cell in row:
                            if isinstance(cell.value, str) and '<' in cell.value and '>' in cell.value:
                                placeholder = cell.value.strip('<>')
                                if placeholder in form.cleaned_data:
                                    cell.value = form.cleaned_data[placeholder]

                output_path = os.path.join(settings.BASE_DIR, 'templates', f'{project_name}_filled.xlsx')
                wb.save(output_path)

                return render(request, 'success_template.html', {'project_name': project_name})
            except Exception as e:
                return HttpResponse(f'Error while processing the workbook: {str(e)}', status=500)
        return render(request, self.template_name, {'form': form, 'project_name': project_name})
