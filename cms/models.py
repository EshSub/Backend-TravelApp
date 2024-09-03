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

class District(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Province(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Image(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    data = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=1000)

    def __str__(self):
        return f"Image {self.id}"

class Image(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    data = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=1000)

    def __str__(self):
        return f"Image {self.id}"

class Place(TimeStampMixin):
    place_id = models.AutoField(primary_key=True)
    place_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    district = models.ForeignKey(District, related_name="places", on_delete=models.PROTECT, null=True, blank=True)
    province = models.ForeignKey(Province, related_name="places", on_delete=models.PROTECT, null=True, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    types = models.ManyToManyField("Type", related_name="places")
    how_to_visit = models.TextField(null=True, blank=True)
    accommodation_places_nearby = models.ManyToManyField("self", related_name="places_nearby", blank=True)
    best_time_to_visit_in_year = models.CharField(max_length=100, null=True, blank=True)
    tags = models.ManyToManyField("Tag", related_name="places", blank=True)
    activities = models.ManyToManyField("Activity", related_name="places", through="PlaceActivity", blank=True)
    data = models.JSONField(null=True, blank=True)
    ratings = models.FloatField(null=True, blank=True)
    header_image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True, blank=True)
    images = models.ManyToManyField(Image, related_name="places")
    ratings = models.FloatField(null=True, blank=True)
    header_image = models.ForeignKey(Image, on_delete=models.PROTECT, null=True, blank=True)
    images = models.ManyToManyField(Image, related_name="places")

    def __str__(self):
        return self.place_name
    
# column1=place_id,column2=place_name,column3=description,column4=district_id,column5=province_id,column6=ticket_price,column7=location,column8=latitude,column9=longitude,column10=how_to_visit,,column11=best_time_to_visit_in_year,,column12=data


class Activity(TimeStampMixin):
    activity_id = models.AutoField(primary_key=True)
    activity_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    data = models.JSONField(null=True, blank=True)
# column1=activity_id,column2=activity_name,column3=description,column4=data
class PlaceActivity(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    place = models.ForeignKey(Place, related_name="place_activities", on_delete=models.PROTECT, null=True, blank=True)
    activity = models.ForeignKey(Activity, related_name="place_activities", on_delete=models.PROTECT, null=True , blank=True)
    description = models.TextField(null=True, blank=True)
    data = models.JSONField(null=True, blank=True)
# column1=id,column2=place_id,column3=activity_id,column4=description,column5=data
class Type(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Tag(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


