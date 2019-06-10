from django.db import models
from datetime import datetime  

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

    def __int__(self):
        return self.idincident

class Log(models.Model):
    username = models.CharField(max_length=30)
    like = models.BooleanField(default=0)
    dislike = models.BooleanField(default=0)
    hits = models.BooleanField(default=0)
    incident = models.ForeignKey('Incident', on_delete=models.CASCADE)

class Komentar(models.Model):
    id_komentar = models.AutoField(primary_key=True)
    nik = models.IntegerField()
    isi_komentar = models.TextField()
    tanggal_komentar = models.DateTimeField(default=datetime.now)
    incident = models.ForeignKey('Incident', on_delete=models.CASCADE)

    def __int__(self):
        return self.id_komentar