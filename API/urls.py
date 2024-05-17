from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginAPi.as_view(), name ="login"),
    path('blog/', BlogAPI.as_view(), name ="Blog"),
    path('blog/<str:slug>', SingleBlogAPI.as_view(), name ="Blog"),
    path('comment/<str:slug>', CommentAPI.as_view(), name ="comment"),
    path('category/', CategoryAPI.as_view(), name ="addcategory"),
    path('category/<int:id>', CategoryAPI.as_view(), name ="addcategory"),
    path('like/<str:slug>', LikeBlogAPI.as_view(), name ="like"),
    path('dlike/<str:slug>', DLikeBlogAPI.as_view(), name ="dlike"),
    path('user/', GetUserDetailsAPI.as_view(), name ="user"),
    path('userblog/', UserBlogAPI.as_view(), name ="userblog"),
    path('logout/', LogoutAPI.as_view(), name ="logout"),
    path('aboutuser/', AboutUserAPI.as_view(), name ="aboutuser"),
    path('account/', AccountAPI.as_view()),
    path('check_email/', CheckEmailAvailability.as_view()),
    path('update_about_you/', UserAboutYouUpdateAPIView.as_view(), name='update_about_you'),
    path('verify-otp-and-update-email/', VerifyOTPAndUpdateEmail.as_view(), name='verify_otp_and_update_email'),
    path('ChangePasswordView/', ChangePasswordView.as_view(), name='ChangePasswordView'),

]