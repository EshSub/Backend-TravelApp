from django.db import models
from cms.models import Place
from django.contrib.auth.models import User

# Create your models here.
class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    isAI = models.BooleanField(default=True)

    def __str__(self):
        return f"Conversation {self.conversation_id} - User {self.user_id}"
    
class Message(models.Model):
    date = models.DateField()
    time = models.TimeField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message = models.TextField() 
    place = models.ForeignKey(Place, null=True, blank=True, on_delete=models.PROTECT)  
    guide = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT) 

    def __str__(self):
        return f"Message in Conversation {self.conversation.conversation_id} on {self.date} at {self.time}"
