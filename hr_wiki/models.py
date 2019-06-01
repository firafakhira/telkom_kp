from django.db import models

# Create your models here.
class Incident(models.Model):
    idincident = models.AutoField(primary_key=True)
    kasus = models.TextField()
    applikasi = models.CharField(max_length=45)
    solusi = models.TextField()
    createdby = models.CharField(max_length=20)
    lastupdate = models.CharField(max_length=30)
    # link = models.CharField(max_length=200)
    # direktori = models.CharField(max_length=500)
    like = models.IntegerField()
    dislike = models.IntegerField()
    # flagdefinisi = models.IntegerField(blank=True, null=True)
    # flagaktif = models.IntegerField(blank=True, null=True)
    # flagapprove = models.IntegerField(blank=True, null=True)
    hits = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.idincident
class Log(models.Model):
    username = models.CharField(max_length=30)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    incident = models.ForeignKey('Incident', on_delete=models.CASCADE)
