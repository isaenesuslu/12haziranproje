from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Reply(models.Model):
    user = models.OneToOneField(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    reply = models.CharField(("Gizli Yanıt"), max_length=50)
    
    def __str__(self):
        return self.user.username