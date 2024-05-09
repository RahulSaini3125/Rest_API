from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .helper import ConvertTextToSlug
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse


# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password,**extra_field):
        if  not email:
            raise ValueError('Email Field is required')
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_field)
        user.set_password(password)
        user.save(using = self.db)
        return user
    
    def create_user(self, email, password = None, **extra_field):
        extra_field.setdefault('is_staff',False)
        extra_field.setdefault('is_superuser', False)
        return self._create_user(email, password,**extra_field)
    
    def create_superuser(self,email, password, **extra_field):
        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)
        if  extra_field.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_field.get('is_superuser') is not True:
            raise ValueError('SuperUser must have is_superuser = True')
        return  self._create_user(email,password,**extra_field)
    

class User(AbstractUser):
    username = None
    otp = models.IntegerField(null = True, blank = True)
    email = models.EmailField(max_length = 50, unique = True)
    bloger_name = models.CharField(max_length = 50, null = True, blank = True)
    aboutYou = models.TextField(max_length = 200, null = True, blank = True)
    user_profile = models.ImageField(upload_to='media/',null = True, blank= True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_absolute_url():
        return reverse('profile')



class CategoryModels(models.Model):
    Category = models.CharField(max_length = 20,unique = True)

    def __str__(self):
        return self.Category

class BlogModels(models.Model):
    Categorys = {
        'Lifestyle': 'LIFESTYLE',
        'Travel': 'TRAVEL',
        'Experience': 'EXPERIENCE',
        'Fashion': 'FASHION',
        'Explore':'EXPLORE'
    }
    Blog_upload_by = models.ForeignKey(User, on_delete = models.CASCADE)
    Blog_title = models.CharField(max_length = 100)
    Blog_description = models.CharField(max_length = 400)
    Blog_slug = models.CharField(max_length = 200, unique = True, null = True, blank = True)
    Blog_content_heading = models.CharField(max_length = 100)
    Blog_content = models.CharField(null=True,blank=True)
    Blog_images = models.ImageField(upload_to='media/')
    Blog_Category = models.ForeignKey(CategoryModels, on_delete = models.PROTECT)
    BLog_upload_date = models.DateField(auto_now_add = True)
    Blog_like = models.ManyToManyField(User, blank = True, related_name='like')

    def save(self,* agrs, ** kwagra):
        if self.Blog_slug is None:
            self.Blog_slug = ConvertTextToSlug(self.Blog_title)
        self.Blog_title = self.Blog_title.capitalize()
        super(BlogModels,self).save(*agrs,**kwagra)

    def get_absolute_url(self):
        return reverse('BlogRead', args=[str(self.Blog_slug)])

    def like_count(self):
        return self.Blog_like.count()
    
    def __str__(self):
        return self.Blog_title

class Comment(models.Model):
    comment = models.CharField(max_length = 1000)
    comment_on = models.DateField(auto_now_add = True)
    blog = models.ForeignKey(BlogModels, on_delete = models.CASCADE)
    comment_by = models.ForeignKey(User, on_delete= models.PROTECT)