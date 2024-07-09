from django.db import models


class Specialty(models.Model):
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return self.specialty

    class Meta:
        verbose_name_plural = "Specialties"
