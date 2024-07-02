from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name="profile", on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
class EmailConfirmation(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="email_confirmation", on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
