from django.contrib import admin

# Register your models here.
from guestbook.models import GuestBook

admin.site.register(GuestBook)