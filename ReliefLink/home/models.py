# home/models.py
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
import random
import string

class PasswordSet:
    def generate_password(self, length=8):
        """Generate a random password with letters, digits, and symbols."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    def send_password_email(self, name, email, raw_password):
        """Send the generated password to the user's email."""
        subject = "Your Account Password"
        message = f"Hello {name},\n\nYour account has been created. Here is your temporary password:\n\n{raw_password}\n\nPlease log in and change your password immediately."
        from_email = "labr1t18203@gmail.com"
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

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

class Housh(models.Model):
    holding_number = models.CharField(max_length=20, blank=True, null=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    familyMember = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.holding_number:
            division_code = self.ward.union.upazila.district.division.name[:2].lower()
            district_code = self.ward.union.upazila.district.name[:2].lower()
            upazila_code = self.ward.union.upazila.name[:2].lower()
            union_code = self.ward.union.name[:2].lower()
            ward_code = self.ward.name[:2].lower()
            house_count = Housh.objects.filter(ward=self.ward).count() + 1
            self.holding_number = f"{division_code}{district_code}{upazila_code}{union_code}{ward_code}{house_count}"

        super().save(*args, **kwargs)


# BaseUserModel to handle shared logic
class BaseUserModel(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    password = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        passwordObj = PasswordSet()
        if not self.pk:
            raw_password = passwordObj.generate_password()
            self.password = make_password(raw_password)
            passwordObj.send_password_email(self.name, self.email, raw_password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class DivisionalCommissionar(BaseUserModel):
    division = models.OneToOneField(Division, on_delete=models.CASCADE)

class DeputyCommissionar(BaseUserModel):
    district = models.OneToOneField(District, on_delete=models.CASCADE)

class UNO(BaseUserModel):
    upazila = models.OneToOneField(Upazila, on_delete=models.CASCADE)

class UnionChairman(BaseUserModel):
    union = models.OneToOneField(Union, on_delete=models.CASCADE)

class WardMember(BaseUserModel):
    ward = models.OneToOneField(Ward, on_delete=models.CASCADE)
