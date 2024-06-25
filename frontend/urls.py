

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
#from frontend.views import UploadExcelView, modify_excel
from .views import ProjectSelectView, FillProjectTemplateView
from .views import AboutView, ProjectSelectView, FillProjectTemplateView

urlpatterns = [
    #path("", views.index, name='home'),  # Root URL pointing to login view
    #path("home/", views.index, name='home'),
    #path("about/", views.about, name='about'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    # path('upload/', UploadExcelView.as_view(), name='upload_excel'),
    # path('modify/', modify_excel, name='modify_excel'),
    path('select_project/', ProjectSelectView.as_view(), name='select_project'),
    path('fill_project_template/<str:project_name>/', FillProjectTemplateView.as_view(), name='fill_project_template'),
    path('about/', AboutView.as_view(), name='about'),
    path('project-select/', ProjectSelectView.as_view(), name='project_select'),
    path('fill-project-template/<str:project_name>/', FillProjectTemplateView.as_view(), name='fill_project_template'),
]
