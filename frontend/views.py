import os
import json
from io import BytesIO
import openpyxl

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django import forms
from django.conf import settings
import requests
import openai

from .forms import InputForm, DynamicForm
from datasets import load_dataset

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
            request.session['project_name'] = project
            return redirect('fill_project_template_step1', project_name=project)
        return render(request, self.template_name, {'form': form})



from django.shortcuts import redirect

class FillProjectTemplateStep1View(View):
    template_name = 'fill_project_template_step1.html'

    def get_placeholder_fields(self, wb):
        placeholders = set()
        for sheet in wb:
            for row in sheet.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str):
                        if '<' in cell.value and '>' in cell.value:
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

        # Dynamically create a form with fields corresponding to placeholders
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

        # Dynamically create a form with fields corresponding to placeholders
        form_class = type('DynamicForm', (DynamicForm,), {placeholder: forms.CharField(label=placeholder) for placeholder in placeholders})
        form = form_class(request.POST)

        if form.is_valid():
            try:
                for sheet in wb:
                    for row in sheet.iter_rows():
                        for cell in row:
                            if isinstance(cell.value, str):
                                if '<' in cell.value and '>' in cell.value:
                                    placeholder = cell.value.strip('<>')
                                    if placeholder in form.cleaned_data:
                                        cell.value = form.cleaned_data[placeholder]

                # Save the filled workbook to BytesIO
                output = BytesIO()
                wb.save(output)
                output.seek(0)

                # # Prepare HTTP response with the filled Excel file
                # response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                # response['Content-Disposition'] = f'attachment; filename="{project_name}_filled.xlsx"'
                # return response

            except Exception as e:
                return HttpResponse(f'Error while processing the workbook: {str(e)}', status=500)

        return redirect('fill_project_template_step2', project_name=project_name)


class FillProjectTemplateStep2View(View):
    def get_placeholder_fields(self, wb):
        placeholders = set()
        for sheet in wb:
            for row in sheet.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str) and '**' in cell.value:
                        placeholders.add(cell.value.strip('**'))
        return placeholders
    

    def send_to_openai(self, text):
        try:
            openai.api_key = 'sk-proj-NxZVgogGgeOB6o1iCeQzT3BlbkFJXHJ1HFruOF6DfOpMJs40'  # Set your OpenAI API key here

            response = openai.Completion.create(
                engine="gpt-3.5-turbo",  # Replace with the appropriate engine name
                prompt=text,
                max_tokens=150
            )

            return response['choices'][0]['text']

        except requests.RequestException as e:
            raise RuntimeError(f'Error communicating with OpenAI API: {str(e)}')

        except Exception as e:
            raise RuntimeError(f'Error with OpenAI API: {str(e)}')


    def get(self, request, project_name):
        template_path = os.path.join(settings.BASE_DIR, 'templates', f'{project_name}.xlsx')
        try:
            wb = openpyxl.load_workbook(template_path)
        except FileNotFoundError:
            return HttpResponse(f'Template file not found: {template_path}', status=404)
        except openpyxl.utils.exceptions.InvalidFileException:
            return HttpResponse(f'Invalid template file: {template_path}', status=400)

        placeholders = self.get_placeholder_fields(wb)

        # Dynamically create a form with fields corresponding to placeholders
        form_class = type('DynamicForm', (forms.Form,), {placeholder: forms.CharField(label=placeholder) for placeholder in placeholders})
        form = form_class()

        return render(request, 'fill_project_template_step2.html', {'form': form, 'project_name': project_name})

    def post(self, request, project_name):
        template_path = os.path.join(settings.BASE_DIR, 'templates', f'{project_name}.xlsx')
        try:
            wb = openpyxl.load_workbook(template_path)
        except FileNotFoundError:
            return HttpResponse(f'Template file not found: {template_path}', status=404)
        except openpyxl.utils.exceptions.InvalidFileException:
            return HttpResponse(f'Invalid template file: {template_path}', status=400)

        placeholders = self.get_placeholder_fields(wb)

        # Dynamically create a form with fields corresponding to placeholders
        form_class = type('DynamicForm', (forms.Form,), {placeholder: forms.CharField(label=placeholder) for placeholder in placeholders})
        form = form_class(request.POST)

        if form.is_valid():
            try:
                for sheet in wb:
                    for row in sheet.iter_rows():
                        for cell in row:
                            if isinstance(cell.value, str) and '**' in cell.value:
                                placeholder = cell.value.strip('**')
                                if placeholder in form.cleaned_data:
                                    # Send cleaned data to OpenAI
                                    ai_response = self.send_to_openai(form.cleaned_data[placeholder])
                                    # Update cell with AI response
                                    cell.value = ai_response.get('choices', [{'text': ''}])[0].get('text', '')  # Adjust based on actual API response structure

                output = BytesIO()
                wb.save(output)
                output.seek(0)

                response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{project_name}_filled.xlsx"'
                return response

            except Exception as e:
                return HttpResponse(f'Error while processing the workbook: {str(e)}', status=500)

        return render(request, 'fill_project_template_step2.html', {'form': form, 'project_name': project_name})