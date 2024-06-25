from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
#from frontend.views import UploadExcelView, modify_excel
from .views import ProjectSelectView
from .views import AboutView, ProjectSelectView
from .views import ProjectSelectView
from .views import FillProjectTemplateStep1View, FillProjectTemplateStep2View

urlpatterns = [
    #path("", views.index, name='home'),  # Root URL pointing to login view
    #path("home/", views.index, name='home'),
    #path("about/", views.about, name='about'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    # path('upload/', UploadExcelView.as_view(), name='upload_excel'),
    # path('modify/', modify_excel, name='modify_excel'),
    path('select_project/', ProjectSelectView.as_view(), name='select_project'),
    
    path('about/', AboutView.as_view(), name='about'),
    path('project-select/', ProjectSelectView.as_view(), name='project_select'),
    path('fill_project_template_step1/<str:project_name>/', FillProjectTemplateStep1View.as_view(), name='fill_project_template_step1'),
    path('fill_project_template_step2/<str:project_name>/', FillProjectTemplateStep2View.as_view(), name='fill_project_template_step2'),
]