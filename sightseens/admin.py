from django.contrib import admin
from .models.Location import Location
from .models.User import User
from .models.Visit import Visit

# Register your models here.
admin.site.register(User)
admin.site.register(Location)
admin.site.register(Visit)
