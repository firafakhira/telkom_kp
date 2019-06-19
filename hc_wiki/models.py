from django.db import models
from datetime import datetime  

# Create your models here.
class Incident(models.Model):
    idincident = models.AutoField(primary_key=True)
    kasus = models.TextField()
    applikasi = models.CharField(max_length=45, default='-')
    solusi = models.TextField()
    createdby = models.CharField(max_length=20)
    lastupdate = models.CharField(max_length=30, default=datetime.now)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    busscd = models.IntegerField(default=1000)

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
