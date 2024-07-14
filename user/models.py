from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from setting.models import Specialty


class CustomAccountManager(BaseUserManager):
    def create_user(
        self, email, username, first_name, last_name, password, **extra_fields
    ):
        if not email:
            raise ValueError("you must provide an email address")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email, username, first_name, last_name, password, **extra_fields
    ):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email, username, first_name, last_name, password, **extra_fields
        )


class Account(AbstractBaseUser, PermissionsMixin):
    GENDERS = {"M": "Male", "F": "Female"}
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDERS)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)
    image = models.ImageField(upload_to="users/", null=True, blank=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Patient(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return "Mr." if self.account.gender == "M" else "Mrs."


class Doctor(models.Model):
    visit_cost = models.IntegerField(default=100_000)
    clinic_address = models.CharField(max_length=255)
    specialty = models.ForeignKey(
        Specialty, on_delete=models.CASCADE, related_name="doctors"
    )
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    avg_rate = models.FloatField(default=0)

    def __str__(self):
        return f"Dr. {self.account.first_name} {self.account.last_name}"


class VisitTime(models.Model):
    WEEK_DAYS = {
        "SAT": "Saturday",
        "SUN": "Sunday",
        "MON": "Monday",
        "TUE": "Tuesday",
        "WED": "Wednesday",
        "THU": "Thursday",
        "FRI": "Friday",
    }
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=3, choices=WEEK_DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"Dr. {self.doctor.account} {self.weekday} {self.start_time}"
