from django.contrib import admin
from django.urls import path
from wipchatbot import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login/', csrf_exempt(views.LoginView.as_view())),
    path('askme/', views.ChatBotView.as_view()),
    path('register/', views.UserRegister.as_view()),
    path('fileupload/', views.UploadFile.as_view()),
]