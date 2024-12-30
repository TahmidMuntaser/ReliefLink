# home/models.py
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string
import logging

logger = logging.getLogger(__name__)

# Define the custom user manager
class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

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
    family_member = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.holding_number:
            try:
                division_code = self.ward.union.upazila.district.division.name[:2].lower()
                district_code = self.ward.union.upazila.district.name[:2].lower()
                upazila_code = self.ward.union.upazila.name[:2].lower()
                union_code = self.ward.union.name[:2].lower()
                ward_code = self.ward.name[:2].lower()
                house_count = Housh.objects.filter(ward=self.ward).count() + 1
                self.holding_number = f"{division_code}{district_code}{upazila_code}{union_code}{ward_code}{house_count}"
            except AttributeError as e:
                logger.error(f"Holding number generation failed for house in ward {self.ward.id}: {e}")
                raise ValueError("Invalid data for holding number generation.")
        super().save(*args, **kwargs)


class PasswordUtility:
    @staticmethod
    def generate_password(length=None):
        """Generate a random password."""
        length = length or getattr(settings, 'PASSWORD_LENGTH', 8)  # Default length is 8
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def send_password_email(name, email, raw_password):
        """Send the generated password to the user's email."""
        subject = "Your Account Password"
        message = (
            f"Hello {name},\n\n"
            f"Your account has been created. Here is your temporary password:\n\n"
            f"{raw_password}\n\n"
            f"Please log in and change your password immediately."
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            logger.error(f"Failed to send email to {email}: {e}")


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('Admin', 'Admin'),
        ('DivisionalCommissioner', 'Divisional Commissioner'),
        ('DeputyCommissioner', 'Deputy Commissioner'),
        ('UNO', 'UNO'),
        ('UnionChairman', 'Union Chairman'),
        ('WardMember', 'Ward Member'),
        ('Public', 'Public'),
    )
    username = None  # Remove the default username field
    email = models.EmailField(unique=True)  # Use email as the username
    name = models.CharField(max_length=100, blank=False, null=False)
    user_type = models.CharField(max_length=30, choices=USER_TYPES)
    division = models.ForeignKey(Division, null=True, blank=True, on_delete=models.SET_NULL)
    district = models.ForeignKey(District, null=True, blank=True, on_delete=models.SET_NULL)
    upazila = models.ForeignKey(Upazila, null=True, blank=True, on_delete=models.SET_NULL)
    union = models.ForeignKey(Union, null=True, blank=True, on_delete=models.SET_NULL)
    ward = models.ForeignKey(Ward, null=True, blank=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    # Use the custom user manager
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.name} ({self.user_type})"
    
    # def clean(self):
    #     if self.user_type in ['Admin', 'DivisionalCommissioner']:
    #         if not self.email.endswith('@organization.com'):
    #             raise ValidationError("Email must belong to @organization.com domain.")
    #     super().clean()


@receiver(post_save, sender=CustomUser)
def handle_new_user(sender, instance, created, **kwargs):
    if created:
        raw_password = PasswordUtility.generate_password()
        instance.set_password(raw_password)
        instance.save()
        PasswordUtility.send_password_email(instance.name, instance.email, raw_password)
