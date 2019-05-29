from django.db import models

# Create your models here.
class Konten(models.Model):
    judul = models.CharField(max_length=50)
    highlight = models.TextField()
    isi = models.TextField()

    def __str__(self):
        return self.judul

class User(models.Model):
    nik = models.IntegerField(primary_key=True)
    nama = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    noHp = models.CharField(max_length=15)
    role = models.CharField(max_length=10)

    def __str__(self):
        return self.nik

class Incident(models.Model):
    idincident = models.AutoField(primary_key=True)
    kasus = models.TextField()
    applikasi = models.CharField(max_length=45)
    solusi = models.TextField()
    createdby = models.CharField(max_length=20)
    lastupdate = models.CharField(max_length=30)
    link = models.CharField(max_length=200)
    direktori = models.CharField(max_length=500)
    flagdefinisi = models.IntegerField(blank=True, null=True)
    flagaktif = models.IntegerField(blank=True, null=True)
    flagapprove = models.IntegerField(blank=True, null=True)
    hits = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.idincident