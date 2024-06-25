from django import forms

class InputForm(forms.Form):
    url = forms.URLField(label='URL', max_length=200)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    search_term = forms.CharField(label='Search Term', max_length=100)
    summary_text = forms.CharField(label='Summary Text', widget=forms.Textarea)
    affected_area = forms.CharField(label='Affected Area', max_length=100)
    company_name = forms.CharField(label='Company Name', max_length=100)
    requested_date = forms.DateField(label='Requested Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    number_of_users = forms.CharField(label='Number of Users', max_length=100)
    affected_services = forms.CharField(label='Affected Services', max_length=100)
    resources_required = forms.CharField(label='Resources Required to Prepare', max_length=100)
    preparation_effort = forms.CharField(label='Preparation Effort', max_length=100)
    implementation_duration = forms.CharField(label='Implementation Duration', max_length=100)
    failure_exposure = forms.CharField(label='Failure Exposure', max_length=100)
