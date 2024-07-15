from django.contrib import admin
from .models import Comment, Reservation

# Register your models here.
admin.site.register(Comment)
admin.site.register(Reservation)
