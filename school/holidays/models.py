from django.db import models

class Holiday(models.Model):
    holiday_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    holiday_type = models.CharField(max_length=100, default='Public Holiday')
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['start_date']