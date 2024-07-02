from django.contrib import admin
from cms.models import Profile, EmailConfirmation

# Register your models here.
admin.site.register(Profile)
admin.site.register(EmailConfirmation)
