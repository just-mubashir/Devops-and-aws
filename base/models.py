from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True , editable=False , default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now= True)
    updated_at = models.DateTimeField(auto_now_add= True)
    class Meta:
        abstract = True

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True , null=True , blank=True)
    category_image = models.ImageField(upload_to="catgories")


    def save(self , *args , **kwargs):
        self.slug = slugify(self.category_name)
        super(Category ,self).save(*args , **kwargs)


# class Profile(BaseModel):
#     user = models.OneToOneField(User , on_delete=models.CASCADE , related_name="profile")
#     first_name = models.CharField(max_length=25)
#     middle_name = models.CharField(max_length=25)
#     last_name = models.CharField(max_length=25)
#     address = models.CharField(max_length=255)
#     city = models.CharField(max_length=100, null=False , blank=False)
#     state = models.CharField(max_length=100, null=False , blank=False)
#     country = models.CharField(max_length=100,default="India", null=False , blank=False)
#     mobile = models.CharField(max_length=15,default="+91", unique=True, null=False , blank=False)
#     email = models.EmailField(max_length=100, default="@gmail.com", unique=True, null=False , blank=False)
#     pincode = models.IntegerField(max_length=6)
#     token = models.CharField(max_length=100)
#     mobile_otp = models.CharField(max_length=100)
#     email_otp = models.CharField(max_length=100)
#     blank1 = models.CharField(max_length=100)
#     blank2 = models.CharField(max_length=100)
#     blank3 = models.CharField(max_length=100)
#     blank4 = models.BooleanField(default=False)
#     blank5 = models.BooleanField(default=False)
#     is_email_verified = models.BooleanField(default=False)
#     email_token = models.CharField(max_length=100 , null=True , blank=True)
#     profile_image = models.ImageField(upload_to = 'profile')
#
#     def __str__(self) -> str:
#         return self.user

class City(BaseModel):
    city_name = models.CharField(max_length=100, default="Mumbai")
    city_code = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.city_name

class State(BaseModel):
    state_name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=3)

    def __str__(self) -> str:
        return self.state_name


class Country(BaseModel):
    country_name = models.CharField(max_length=15, default="India")
    country_code = models.CharField(max_length=3, default="IND",null=False , blank=False,)

    def __str__(self) -> str:
        return self.country_name


class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title + "\n" + self.description

# @receiver(post_save , sender = User)
# def  send_email_token(sender , instance , created , **kwargs):
#     try:
#         if created:
#             email_token = str(uuid.uuid4())
#             Profile.objects.create(user = instance , email_token = email_token)
#             email = instance.email
#             send_account_activation_email(email , email_token)
#
#     except Exception as e:
#         print(e)
#
#
# from django.conf import settings
# from django.core.mail import send_mail
#
# def send_account_activation_email(email , email_token):
#     return
#         subject = 'Your account needs to be verified'
#         email_from = settings.EMAIL_HOST_USER
#         message = f'Hi, click on the link to activate your account http://127.0.0.1:8000/accounts/activate/{email_token}'
#         send_mail(subject , message , email_from , [email])