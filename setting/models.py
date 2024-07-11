from django.db import models


def specialty_image_directory_path(instance, filename):
    return "specialties/{0}".format(instance.specialty)


class Specialty(models.Model):
    specialty = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to=specialty_image_directory_path, blank=False, null=True
    )

    def __str__(self):
        return self.specialty

    class Meta:
        verbose_name_plural = "Specialties"
