from django.db import models

class Add_court(models.Model):
    cname=models.CharField(max_length=100)
    cloc=models.CharField(max_length=255)
    jurisdiction=models.CharField(max_length=255)
    year=models.IntegerField()
    chiefjustice = models.CharField(max_length=255)
    noj = models.CharField(max_length=255)
    image=models.ImageField(upload_to="court/")



class Add_law(models.Model):
    law_section=models.CharField(max_length=100)
    description=models.CharField(max_length=255)
    penalty=models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    amendment_details = models.CharField(max_length=255)
    provisions = models.CharField(max_length=255)
    year_enacted=models.IntegerField()
    applicability = models.CharField(max_length=255)

