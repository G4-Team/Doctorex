from django.contrib import admin

from .models import Comment, Reservation, VisitTime

admin.site.register(Comment)
admin.site.register(Reservation)
admin.site.register(VisitTime)
