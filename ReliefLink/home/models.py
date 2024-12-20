# home/models.py
from django.db import models

class YourModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Division(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Upazila(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Union(models.Model):
    name = models.CharField(max_length=100)
    upazila = models.ForeignKey(Upazila, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Ward(models.Model):
    name = models.CharField(max_length=100)
    union = models.ForeignKey(Union, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class DivisionalCommissionar(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    division = models.OneToOneField(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class DeputyCommissionar(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    district = models.OneToOneField(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class UNO(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    upazila = models.OneToOneField(Upazila, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UnionChairman(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    union = models.OneToOneField(Union, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WardMember(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    ward = models.OneToOneField(Ward, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
