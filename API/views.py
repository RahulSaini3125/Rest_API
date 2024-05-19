from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import BlogModels, Comment, CategoryModels, User
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
# Create your views here.

class AccountAPI(APIView):
    def post(self, request):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            first_name = serializer.validated_data.get('first_name', '')  # Extract first_name if available
            last_name = serializer.validated_data.get('last_name', '')  # Extract last_name if available
            # Create the user
            User = get_user_model()  # Get the custom user model
            user = User.objects.create_user(email=email, password=password, first_name = first_name,last_name=last_name)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            user = User.objects.get(id = request.user.id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except get_user_model().DoesNotExist:
                return Response({"error": "User notuuuuuuuuuuuuuuuu found."}, status=status.HTTP_404_NOT_FOUND)
        

class LoginAPi(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                access = RefreshToken.for_user(user= user)
                return Response(status=status.HTTP_202_ACCEPTED, data={"token": str(access.access_token),'refresh_token':str(access)})
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED,data={'message': 'Invalid credentials'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            refresh_token_obj = RefreshToken(refresh_token)
            refresh_token_obj.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})

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
            data = commentserializers.data
            for d in data:
                for u in user:
                    if d['comment_by'] == u.id:
                        d['comment_by'] = u.get_full_name()
                        break
                else:
                        d['comment_by'] = 'Unkown'
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
    

class AboutUserAPI(APIView):
    def get(self,request):
        try:
            id = request.GET.get('id')
            Users = User.objects.get(user_id = id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'error':'User Not Found','status':status.HTTP_400_BAD_REQUEST})
        try: 
            serializer_user = UserModelSerializer(Users,context ={'request':request})
            category =  CategoryModels.objects.all()
            search = request.GET.get('search')
            blog = BlogModels.objects.filter(Blog_upload_by = Users)
            serializer_blog  = BlogModelsSerializer(blog, many = True, context={'request':request})
            data = serializer_blog.data
            for da in data:
                for cat in category:
                        if da['Blog_Category'] == cat.id:
                            da['Blog_Category']= cat.Category
                            break
                else:
                            da['Blog_Category'] = None
                return Response(status=status.HTTP_200_OK,data={'message':'Successfully','data':{'user':serializer_user.data,'blog':data}})
        except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST,data={'error':'Something Went Wrong'})
        

class CheckEmailAvailability(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = EmailAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            User = get_user_model()
            try:
                # Check if the email is already registered
                user = User.objects.get(email=email)
                return Response({"available": False}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # If email is available, generate OTP and store it in the current user object
                otp = self.generate_otp()
                user = request.user
                user.otp = otp
                user.save()
                subject = 'Your OTP for verification'
                message = f'Your OTP is: {otp}'
                recipient_list = [email]
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,  # Sender's email (configured in settings)
                    recipient_list,
                    fail_silently=False,
                    )
                return Response({"available": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_otp(self):
        # Generate a random 6-digit OTP
        return str(randint(100000, 999999))
    


class UserAboutYouUpdateAPIView(APIView):
    def put(self, request, *args, **kwargs):
        user = request.user  # Assuming the user is authenticated
        serializer = UserAboutYouUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyOTPAndUpdateEmail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            new_email = serializer.validated_data['new_email']
            otp = int(serializer.validated_data['otp'])
            user = request.user

            # Check if the new email is already registered
            if get_user_model().objects.exclude(pk=user.pk).filter(email=new_email).exists():
                return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)
            if user.otp == otp:
                user.email = new_email
                user.save()
                return Response({"message": "Email updated successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=203)

            user.set_password(serializer.data.get("new_password"))
            user.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change

            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CheckEmailAvailabilityPassword(APIView):
    def post(self, request):
        email = request.POST.get('email')
        User = get_user_model()
        try:
                # Check if the email is already registered
                user = User.objects.get(email=email)
                otp = self.generate_otp()
                user.otp = otp
                user.save()
                subject = 'Your OTP for verification'
                message = f'Your OTP is: {otp}'
                recipient_list = [email]
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,  # Sender's email (configured in settings)
                    recipient_list,
                    fail_silently=False,
                    )
                return Response({"available": True}, status=status.HTTP_200_OK)
               
        except User.DoesNotExist:
                # If email is available, generate OTP and store it in the current user object
                return Response({"available": False}, status=status.HTTP_200_OK)

    def generate_otp(self):
        # Generate a random 6-digit OTP
        return str(randint(100000, 999999))



class VerifyOTP(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            new_email = serializer.validated_data['new_email']
            otp = int(serializer.validated_data['otp'])
            user = User.objects.get(email=new_email)
            # Check if the new email is already registered
            if get_user_model().objects.filter(email=new_email).exists():
                pass
            else:
                return Response({"error": "Email not registered."}, status=status.HTTP_400_BAD_REQUEST)
            if user.otp == otp:
                return Response({"message": "OTP Verify Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgetPasswordView(APIView):
    def post(self,request):
        try:
            data = request.data
            user = User.objects.get(email = data['old_password'])
            user.set_password(data['new_password'])
            user.save()
            return Response(status=status.HTTP_200_OK,data='Ok')
        except User.DoesNotExist:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,data={'error':'Email is not registered'})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'error':'Something Went Wrong'})


class UserProfileImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            user_profile= User.objects.get(id=request.user.id)
            serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,data={'error':'Something Went Wrong'})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST,data={'error':'Something Went Wrong'})