from django.utils.text import slugify
import random
import string

def Generators(length):
    text = ''.join(random.choices(string.ascii_lowercase , k=length))
    return text

def ConvertTextToSlug(text):
    NewSlug = slugify(text)
    from .models import BlogModels
    if BlogModels.objects.filter(Blog_slug = NewSlug).first():
        return ConvertTextToSlug(text+ '-' + Generators(10))
    return NewSlug