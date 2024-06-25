

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from frontend.views import UploadExcelView, modify_excel

urlpatterns = [
    #path("", views.index, name='home'),  # Root URL pointing to login view
    #path("home/", views.index, name='home'),
    path("about/", views.about, name='about'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('upload/', UploadExcelView.as_view(), name='upload_excel'),
    path('modify/', modify_excel, name='modify_excel'),
]
