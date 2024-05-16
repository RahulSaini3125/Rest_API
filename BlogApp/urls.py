from django.urls import path
from .views import *

urlpatterns = [
    path('', SignUp_views, name ="SignUp"),
    path('login/', Login_views, name ="Login"),
    path('index/', Home_views, name ="Home"),
    path('Logout/', logout_views, name='Logout'),
    path('ResetPassword/', ResetPass_views, name='ResetPassword'),
    path('VerfiyOtp/<str:email>', OtpVerify_views, name='Verfiy'),
    path('ForgetPassword/<str:email>', changepassword_views, name='changePassword'),
    path('Change/', change_views, name='change'),
    path('Blog/', BlogView_view, name='BlogRead'),
    path('About/', about_view, name='About'),
    path('Contact/', Contact_view, name='Contact'),
    path('Profile/', Profile_view, name='profile'),
    path('UploadBlog/', UploadBlog_view, name='Upload'),
    path('Delete/', delete_view, name='Delete'),
    path('DeleteAccount/', delete_account_view, name='DeleteAccount'),
    path('EditBlog/', EditBlog_view, name='Edit'),
    path('Category/', Category_view, name='Category'),
    path('AboutUser/', AboutUser_View, name='AboutUser'),
]   