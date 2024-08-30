from django.db import models
from cms.models import Place
from django.contrib.auth.models import User

# Create your models here.
class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    isAI = models.BooleanField(default=True)

    def __str__(self):
        return f"Conversation {self.id} - User {self.user}"
    
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message = models.TextField() 
    place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.PROTECT)  
    guide = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT) 

    def __str__(self):
        return f"Message {self.id} in Conversation {self.conversation} on {self.date} at {self.time}"
