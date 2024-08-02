from django.db import models


# Create your models here.
class ACIManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class ACIModel(models.Model):
    class Meta:
        app_label = 'shared'
        abstract = True

    deleted = models.BooleanField(default=False)
    aci_objects = ACIManager()

