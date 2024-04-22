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
]