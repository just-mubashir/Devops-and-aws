from django.contrib import admin

# Register your models here.
from . models import  City,State,Country,Category,Post,Profile,Room,Message

admin.site.register(City)
admin.site.register(State)
admin.site.register(Country)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(Message)