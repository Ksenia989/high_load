from django.contrib import admin
from  .models import Location, User, Visit

# Register your models here.
admin.site.register(User)
admin.site.register(Location)
admin.site.register(Visit)


