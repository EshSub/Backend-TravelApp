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

class Place(TimeStampMixin):
    place_id = models.AutoField(primary_key=True)
    place_name = models.CharField(max_length=255)
    description = models.TextField()
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    how_to_visit = models.TextField()
    accommodation_places_nearby = models.TextField()
    best_time_to_visit_in_year = models.CharField(max_length=100)
    tags = models.CharField(max_length=255)
    activities = models.ManyToManyField("Activity", related_name="places", through="PlaceActivity")
    data = models.JSONField()

class Activity(TimeStampMixin):
    activity_id = models.AutoField(primary_key=True)
    activity_name = models.CharField(max_length=255)
    description = models.TextField()
    data = models.JSONField()

class PlaceActivity(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    place = models.ForeignKey(Place, related_name="place_activity", on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, related_name="place_activity", on_delete=models.CASCADE)
    description = models.TextField()
    data = models.JSONField()
