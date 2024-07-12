from django.db import models


class Specialty(models.Model):
    specialty = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to="specialties/", blank=False, null=True)

    def __str__(self):
        return self.specialty

    class Meta:
        verbose_name_plural = "Specialties"
