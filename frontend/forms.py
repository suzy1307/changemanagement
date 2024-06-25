from django import forms

class InputForm(forms.Form):
    url = forms.URLField(label='URL', widget=forms.URLInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    search_term = forms.CharField(label='Search Term', widget=forms.TextInput(attrs={'class': 'form-control'}))
    summary_text = forms.CharField(label='Summary Text', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    affected_area = forms.CharField(label='Affected Area', widget=forms.TextInput(attrs={'class': 'form-control'}))
    company_name = forms.CharField(label='Company Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    requested_date = forms.DateField(label='Requested Date', widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))
    end_date = forms.DateField(label='End Date', widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))
    number_of_users = forms.CharField(label='Number of Users', widget=forms.TextInput(attrs={'class': 'form-control'}))
    affected_services = forms.CharField(label='Affected Services', widget=forms.TextInput(attrs={'class': 'form-control'}))
    resources_required = forms.CharField(label='Resources Required', widget=forms.TextInput(attrs={'class': 'form-control'}))
    preparation_effort = forms.CharField(label='Preparation Effort', widget=forms.TextInput(attrs={'class': 'form-control'}))
    implementation_duration = forms.CharField(label='Implementation Duration', widget=forms.TextInput(attrs={'class': 'form-control'}))
    failure_exposure = forms.CharField(label='Failure Exposure', widget=forms.TextInput(attrs={'class': 'form-control'}))
