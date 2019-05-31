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