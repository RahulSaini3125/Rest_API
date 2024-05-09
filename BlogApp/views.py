from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
import random
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
# Create your views here.
 
# #########################################################################################
def SignUp_views(request):
    return render(request,'login_signUp/SignUp.html')


# #########################################################################################
def Login_views(request):
    return render(request, 'login_signUp/Login.html')


def Home_views(request):
    from API.models import BlogModels
    blog = BlogModels.objects.all()
    return render(request,'blog1/index.html',{'blogs':blog})


# #########################################################################################
def BlogView_view(request):
    from API.models import BlogModels
    blog = BlogModels.objects.all()
    return render(request, 'base/blog-single.html')



# #########################################################################################
def logout_views(request):
    logout(request)
    return redirect('Login')



# #########################################################################################
def ResetPass_views(request):

    return render(request, 'login_signUp/resetpassword.html')



# #########################################################################################
def OtpVerify_views(request):

    return render (request,'login_signUp/verfiyotp.html')


# #########################################################################################
def changepassword_views(request):

    return render(request, 'login_signUp/changepassword.html')


# #########################################################################################
def change_views(request):

    return render(request, 'login_signUp/change.html')


# #########################################################################################
def about_view(request):
        return render(request, 'base/about.html')


# #########################################################################################
def Contact_view(request):

    return render(request, 'base/contact.html')


# #########################################################################################
def Profile_view(request):

    return render(request, 'base/Profile.html')


# #########################################################################################
def UploadBlog_view(request):

    return render(request,'base/UploadBlog.html')


# #########################################################################################
def EditBlog_view(request):

    return render(request, 'base/editblog.html')


# #########################################################################################
def delete_view(request):

    return render(request, 'base/deleteblog.html')


# #########################################################################
def Category_view(request):

    return render(request, 'base/Category.html')

def AboutUser_View(request):

    return render(request,'base/aboutUser.html')