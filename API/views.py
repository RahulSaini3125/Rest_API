from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import BlogModels, Comment, CategoryModels, User
from .serializers import BlogModelsSerializer, LoginSerializer, CommentSerializer, CategoryModelsSerializer, UserModelSerializer
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    # Get All Blog Method
    def get(self,request):
        category =  CategoryModels.objects.all()
        filter = request.GET.get('Category')
        search = request.GET.get('search')
        if search:
           blog = BlogModels.objects.filter(Blog_title__icontains=search)
        elif filter:
            for cate in category:
                if cate.Category == filter:
                    blog = BlogModels.objects.filter(Blog_Category = cate)
                else :
                    blog = BlogModels.objects.all()
        else:
            blog = BlogModels.objects.all()
        serializer  = BlogModelsSerializer(blog, many = True, context={'request':request})
        data = serializer.data
        for da in data:
            for cat in category:
                    if da['Blog_Category'] == cat.id:
                        da['Blog_Category']= cat.Category
                        break
            else:
                        da['Blog_Category'] = None
        return Response(status = status.HTTP_200_OK,data=data)
    
    # Add Blog Method
    def post(self, request):
        data = request.data.copy()
        data['Blog_upload_by'] = request.user.id
        serializer = BlogModelsSerializer(data= data)
        if serializer.is_valid():
            upload = serializer.save()
            serializer = BlogModelsSerializer(upload,context = {'request':request})
            return Response(status= status.HTTP_201_CREATED, data={'message':'Your Blog Is Created Successfully','data':serializer.data})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=serializer.errors)

class SingleBlogAPI(APIView):
    # # Get One Blog Details
    def get(self,request, slug):
        try:
            blog_obj = BlogModels.objects.get(Blog_slug = slug)
            category =  CategoryModels.objects.all()
            user = User.objects.all()
            serializer = BlogModelsSerializer(blog_obj,context ={'request':request})
            data = serializer.data
            for cat in category:
                if data['Blog_Category'] == cat.id:
                    data['Blog_Category_name']= cat.Category
                    break
            else:
                    data['Blog_Category_name'] = None
            for u in user:
                if data['Blog_upload_by'] == u.id:
                    data['Blog_upload_by_name'] = u.get_full_name()
            data['user_id'] = request.user.id
            user_blog  = User.objects.get(id = data['Blog_upload_by'])
            serializer_user = UserModelSerializer(user_blog,context={'request':request})
            response = {
                'blog':data,
                'user':serializer_user.data
            }
            return Response(status= status.HTTP_200_OK,data= {"Blog":response} )
        except Exception as e:
            return Response(status= status.HTTP_400_BAD_REQUEST,data={'message':str(e)})
    # Update Blog
    def put(self,request, slug, format = None):
        try:
            print(request.data)
            blog = BlogModels.objects.get(Blog_slug = slug)
            serializer = BlogModelsSerializer(blog,data=request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_202_ACCEPTED,data=serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':serializer.errors})
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
            comment = Comment.objects.filter(blog = blog).order_by('-id')
            user = User.objects.all()
            commentserializers = CommentSerializer(comment, many = True)
            print(commentserializers.data)
            data = commentserializers.data
            for d in data:
                for u in user:
                    if d['comment_by'] == u.id:
                        d['comment_by'] = u.get_full_name()
                        break
                else:
                        d['comment_by'] = 'Unkown'
            print(data)
            return Response(status= status.HTTP_200_OK,data=data)
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
            serial = BlogModelsSerializer(blog)
            data = serial.data
            data['user_id'] = request.user.id
            return Response(status=status.HTTP_202_ACCEPTED,data={'message':'Blog Like Successfully','data':data})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':'Something Went Wrong'}) 
        
class DLikeBlogAPI(APIView):
    def post(self,request,slug):
        try:
            blog = BlogModels.objects.get(Blog_slug = slug)
            blog.Blog_like.remove(request.user)
            blog.save()
            serial = BlogModelsSerializer(blog)
            data = serial.data
            data['user_id'] = request.user.id
            return Response(status=status.HTTP_202_ACCEPTED,data={'message':'Blog DisLike Successfully','data':data})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'message':'Something Went Wrong'}) 

# class LogoutAPI(APIView)     

class GetUserDetailsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        try:
            Users = User.objects.get(id = request.user.id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'error':'User Not Found','status':status.HTTP_400_BAD_REQUEST})
        try: 
            serializer = UserModelSerializer(Users,context ={'request':request})

            return Response(status=status.HTTP_200_OK,data={'message':'Successfully','data':serializer.data})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'error':'Something Went Wrong'})
        
class UserBlogAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        category =  CategoryModels.objects.all()
        filter = request.GET.get('Category')
        search = request.GET.get('search')
        blog = BlogModels.objects.filter(Blog_upload_by = request.user)
        serializer  = BlogModelsSerializer(blog, many = True, context={'request':request})
        data = serializer.data
        for da in data:
            for cat in category:
                    if da['Blog_Category'] == cat.id:
                        da['Blog_Category']= cat.Category
                        break
            else:
                        da['Blog_Category'] = None
        return Response(status = status.HTTP_200_OK,data=data)