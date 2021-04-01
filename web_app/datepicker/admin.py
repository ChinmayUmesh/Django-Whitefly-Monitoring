from django.contrib import admin
from .models import Post
from .models import Dates

# Admin Username: grains
# Admin Password: snoopy

admin.site.register(Post)
admin.site.register(Dates)