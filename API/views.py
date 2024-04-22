from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import BlogModels, Comment, CategoryModels
from .serializers import BlogModelsSerializer, LoginSerializer, CommentSerializer, CategoryModelsSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


class LoginAPi(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                access = RefreshToken.for_user(user= user)
                return Response(status=status.HTTP_202_ACCEPTED, data={"token": str(access.access_token)})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED,data={'message': 'Invalid credentials'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

class BlogAPI(APIView):
    permission_classes = [IsAuthenticated]
    # Get All Blog Method
    def get(self,request):
        blog = BlogModels.objects.all()
        serializer  = BlogModelsSerializer(blog, many = True)
        return Response(status = status.HTTP_200_OK,data=serializer.data)
    
    # Add Blog Method
    def post(self, request):
        serializer = BlogModelsSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status= status.HTTP_201_CREATED, data={'message':'Your Blog Is Created Successfully'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=serializer.errors)

class SingleBlogAPI(APIView):
    # # Get One Blog Details
    def get(self,request, slug):
        try:
            blog_obj = BlogModels.objects.get(Blog_slug = slug)
            serializer = BlogModelsSerializer(blog_obj)
            comment_obj = Comment.objects.filter(blog = blog_obj)
            commentserializer = CommentSerializer(comment_obj, many = True)
            return Response(status= status.HTTP_200_OK,data= {"Blog":serializer.data,"comment":commentserializer.data} )
        except Exception as e:
            return Response(status= status.HTTP_400_BAD_REQUEST,data={'message':"Did't Not Found Blog"})
    # Update Blog
    def patch(self,request, slug, format = None):
        try:
            blog = BlogModels.objects.get(Blog_slug = slug)
            serializer = BlogModelsSerializer(blog,data=request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED,data=serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':'Update Blog is Successfully'})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':'Something Went Wrong'})
    # Delete Blog
    def delete(self,request, slug):
        try:
            blog_obj = BlogModels.objects.get(Blog_slug= slug)
            blog_obj.delete()
            return Response(status=status.HTTP_200_OK,data={'message':'Blog Is Delete Successfully'})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':str(e)})

class CommentAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,slug):
        try:
            blog = BlogModels.objects.get(Blog_slug=slug)
            comment = Comment.objects.filter(blog = blog)
            commentserializers = CommentSerializer(comment, many = True)
            return Response(status= status.HTTP_200_OK,data=commentserializers.data)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':str(e)})
    
    def post(self,request,slug):
        blog = BlogModels.objects.get(Blog_slug=slug)
        request.data._mutable = True
        # real_data = request.data
        # print(real_data)
        request.data['blog'] = blog.pk
        request.data['comment_by'] = request.user.pk
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,data={'message':'Comment Add Successfully'})
        else:
            return Response(status=status.HTTP_200_OK, data=serializer.errors)

        

class CategoryAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer = CategoryModelsSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,data={'message':'Category Add Successfully'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=serializer.errors)
        
    def get(self,request):
        Category = CategoryModels.objects.all()
        serializer = CategoryModelsSerializer(Category, many = True)
        return Response(status= status.HTTP_200_OK, data=serializer.data)

    # class DeleteCategoryAPI(APIView):
    def delete(self,request, id):
        try:
            Category = CategoryModels.objects.get(id =id)
            Category.delete()
            return Response(data={'message':'Category Delete Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'message':str(e)},status=status.HTTP_400_BAD_REQUEST)

class LikeBlogAPI(APIView):
    def post(self,request,slug):
        try:
            blog = BlogModels.objects.get(Blog_slug = slug)
            blog.Blog_like.add(request.user)
            blog.save()
            return Response(status=status.HTTP_202_ACCEPTED,data={'message':'Blog Like Successfully'})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':'Something Went Wrong'}) 
        
class DLikeBlogAPI(APIView):
    def post(self,request,slug):
        try:
            blog = BlogModels.objects.get(Blog_slug = slug)
            blog.Blog_like.remove(request.user)
            blog.save()
            return Response(status=status.HTTP_202_ACCEPTED,data={'message':'Blog DisLike Successfully'})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':'Something Went Wrong'}) 