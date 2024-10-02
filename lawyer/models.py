from django.db import models
from django.contrib.auth.models import User
# from user.models import Contact_lawyer
# Create your models here.

class Lawyer_Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    license_no = models.CharField(max_length=200)
    address=models.TextField()
    city=models.CharField(max_length=255)
    aop=models.CharField(max_length=255)
    description = models.TextField()
    cop = models.CharField(max_length=255)
    image=models.ImageField(upload_to="image/")
    status = models.BooleanField(default=False)

class Reply(models.Model):
    # complaint=models.ForeignKey(Contact_lawyer,on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer_Profile, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply= models.TextField()