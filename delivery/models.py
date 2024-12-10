from django.db import models

class Restaurant(models.Model):
    id = models.IntegerField(primary_key=True)
    latitude = models.FloatField(null= True)
    longitude = models.FloatField(null=True)
    availability_radius = models.FloatField(null=True)
    open_hour = models.TimeField(null=True)
    close_hour = models.TimeField(null=True)
    rating = models.IntegerField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
        ]

    def __str__(self):
        return f"Restarant Id {self.id} ,Latitude {self.latitude},Longitude {self.longitude}"

