from django.db import models
from django.contrib.auth.models import User


class Voter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    house = models.CharField()
    dob = models.CharField()
    aadhaar = models.CharField(max_length=12, unique=True, null=True, blank=True)
    casted_vote = models.BooleanField(default=False)

class Candidate(models.Model):
    name = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='candidates')
    votes = models.IntegerField(default=0)
