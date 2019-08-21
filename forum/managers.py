from django.db import models
from .models import Profile, Project


class ProfileManager(models.Manager):
    
    def get_queryset(self):
        pass
        


